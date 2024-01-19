import torch
import torchvision
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
from torchvision.transforms.functional import to_pil_image, crop
import torch.nn as nn
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from typing import *

from pipeline.Unnormaliz import UnNormalize

PART_LABEL = {
    "upper":[4, 7],
    "lower":[5, 6],
    #"shoes":[9, 10],
    #"hat":[1],
    "hair": [2],
    "skin": [11, 12, 13, 14, 15],
}

COLOR_SPACE_MAP = {
    'GrayScale':1,
    'RGB':3,
    'RGBA':4
}

class FeaturingModel:
    def __init__(self,
                 useGPU: bool = False,
                 segformer_path: str = "mattmdjaga/segformer_b2_clothes",
                 classifier_path: str = "./checkpoint/classifier_mobilenetv3.pt",
                 classifier_input_size: int = 448
                 ):
        self.cpu_device = torch.device("cpu")
        self.device = torch.device("cpu")
        if useGPU and torch.cuda.is_available():
            self.device = torch.device("cuda")


        self.segformer_processor = SegformerImageProcessor.from_pretrained(segformer_path)
        self.segformer_model = AutoModelForSemanticSegmentation.from_pretrained(segformer_path)

        self.classifier_model = torch.load(classifier_path, map_location=self.device)
        self.classifier_model = self.classifier_model.features

        self.classifier_input_size = classifier_input_size

        self.topilimage = torchvision.transforms.ToPILImage()
        self.totensor = torchvision.transforms.ToTensor()

        self.transformer = transforms.Compose([transforms.ToTensor(),
                                          torchvision.transforms.Resize((self.classifier_input_size)*2),
                                          transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                                          ])
        self.unnormalize = UnNormalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])


    def getPart(self,
                image_ori: Image.Image,
                seg: torch.tensor,
                labels: List[int],
                image_channel: int = 3,
                background: int = 0):
        mask = seg==labels[0]
        if len(labels)>=2:
            for label in labels[1:]:
                mask = torch.logical_or(mask, seg==label)
        masks = torch.stack([mask]*image_channel, dim=0)
        y, x = torch.where(mask)

        image = self.totensor(image_ori)
        image[~masks] = background
        image = self.topilimage(crop(image, torch.min(y), torch.min(x), torch.max(y)-torch.min(y), torch.max(x)-torch.min(x)))

        return image, masks

    def gram_matrix(self, x):
        n, c, h, w = x.size()
        x = x.view(n * c, h * w)
        gram = torch.mm(x, x.t())
        return gram

    def __call__(self, x: str, color_space: str = "RGB"):
        image = Image.open(x).convert(color_space)

        # 전신 사진 분할
        inputs = self.segformer_processor(images=image, return_tensors="pt")
        outputs = self.segformer_model(**inputs)
        logits = outputs.logits.cpu()
        upsampled_logits = nn.functional.interpolate(
            logits,
            size=image.size[::-1],
            mode="bilinear",
            align_corners=False,
        )
        pred_seg = upsampled_logits.argmax(dim=1)[0]

        # 분할 사진 Feature 추출 - 옷
        result = {}
        for name, labels in PART_LABEL.items():
            features = {}
            part_image = self.getPart(image, pred_seg, labels, image_channel=COLOR_SPACE_MAP[color_space])[0]
            input_classifier = self.transformer(part_image).unsqueeze(0).to(self.device)
            output_classifier = self.classifier_model(input_classifier)

            features["last_activation_map"] = torch.flatten(output_classifier).to(self.cpu_device)
            features["gram_matrix"] = self.gram_matrix(output_classifier).to(self.cpu_device)
            features["average_rgb"] = 255*self.unnormalize(input_classifier).squeeze(0).mean(dim=-1).mean(dim=-1)

            result[name] = features

        return result

if __name__=="__main__":
    model = FeaturingModel()
    feature = model("../test_image/test.jpg")
    print(feature["hair"]["average_rgb"])