import torch
import torchvision
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import torch.nn.functional as F
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from typing import *

class FeaturingModel(nn.Module):
    def __init__(self,
                 segformer_path: str = "mattmdjaga/segformer_b2_clothes",
                 classifier_path: str = "./classifier_mobilenetv3.pt",
                 original_class_num: int = 19,
                 classifier_input_size: int = 448
                 ):
        super().__init__()

        self.segformer_processor = SegformerImageProcessor.from_pretrained(segformer_path)
        self.segformer_model = AutoModelForSemanticSegmentation.from_pretrained(segformer_path)

        self.classifier_model = models.mobilenet_v3_large(num_classes=original_class_num)
        self.classifier_model.load_state_dict(classifier_path)
        self.classifier_model = self.classifier_model.features

        self.classifier_input_size = classifier_input_size

    def forward(self, x):
        pass