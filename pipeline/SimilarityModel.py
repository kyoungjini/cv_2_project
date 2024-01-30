import torch
import torchvision
from PIL import Image
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
from torchvision.transforms.functional import to_pil_image, crop
import torch.nn as nn
from typing import *
from colorsys import rgb_to_hsv, hsv_to_rgb
from pipeline.FeaturingModel import FeaturingModel

LAST_ACTIVATION_VOLUME = "last_activation_volume"
GRAM_MATRIX = "gram_matrix"
AVERAGE_RGB = "average_rgb"


class SimilarityModel:
    def __init__(self,
                 recommended,
                 featuring_model: FeaturingModel,
                 useGPU: bool = False,
                 alpha: List[int] = [1, 1, 1]):
        """
        유사도를 계산하여 추천 랭킹을 받는 클래스의 생성자입니다.


        :param recommended: 상의, 하의에 대한 정보와 각 옷의 특징 파일 경로
                            예를 들어, recommended = {"upper":["./pipeline/features/feature0.pt", "./pipeline/features/feature1.pt"], "lower":["./pipeline/features/feature2.pt"]}
        :param featuring_model: 유저의 입력 사진에 대해 특징 추출하는 모델.
        :param useGPU: 연산 시에 GPU를 이용할 것인가.
        :param alpha: 각 유사도의 가중합 계산 시 이용되는 가중치 상수입니다.
        """
        self.cpu_device = torch.device("cpu")
        self.device = torch.device("cpu")
        if useGPU and torch.cuda.is_available():
            self.device = torch.device("cuda")

        self.recommended = recommended
        self.featuring_model = featuring_model
        self.featuring_model.changeDevice(useGPU)

        self.cosine_similarity_model = lambda x, y: (F.cosine_similarity(x, y)+1)/2
        self.l1_similarity_model = lambda x, y: F.tanh(1/(F.l1_loss(x, y) + (1e-8)))

        self.personal_color_type = ["WSB", "WSL", "WAD", "WAM", "CSL", "CSM", "CWB", "CWD"]

        self.alpha = alpha


    def getPersonalColor(self, user_input_features):
        average_rgb = user_input_features[0]["average_rgb"]
        for feature in user_input_features[1:]:
            average_rgb += feature["average_rgb"]
        average_rgb /= len(user_input_features)
        average_rgb = average_rgb.tolist()

        average_hsv = rgb_to_hsv(*average_rgb)
        H = float(average_hsv[0])
        S = float(average_hsv[1])
        V = float(average_hsv[2])
        diff = round(V - S, 2)

        ans = -1
        if H >= 23 and H <= 203:
            if diff >= 46.25:
                if S >= 31.00:
                    ans = 0
                    # Warm Spring Bright
                else:
                    ans = 1
                    # Warm Spring Light

            elif diff < 46.25:
                if S >= 46.22:
                    ans = 2
                    # Warm Autumn Deep
                else:
                    ans = 3
                    # Warm Autumn Mute

        elif (H >= 0 and H < 23) or (H > 203 and H <= 360):
            if diff >= 48.75:
                if diff >= 28.47:
                    ans = 4
                    # Cool Summer Light
                else:
                    ans = 5
                    # Cool Summer Mute

            elif diff < 48.75:
                if diff >= 31.26:
                    ans = 6
                    # Cool Winter Bright
                else:
                    ans = 7
                    # Cool Winter Deep

        else:
            ans = -1
            # 에러

        return self.personal_color_type[ans]


    def getSimilarity(self, user_feature, target_input, type, personal_color: torch.tensor):
        target_feature = torch.load(target_input, map_location=self.device)

        last_activation_volume_similarity = self.cosine_similarity_model(
            torch.flatten(user_feature[type][LAST_ACTIVATION_VOLUME]),
            torch.flatten(target_feature[type][LAST_ACTIVATION_VOLUME]))
        gram_matrix_similarity = self.l1_similarity_model(user_feature[type][GRAM_MATRIX],
                                                          target_feature[type][GRAM_MATRIX])
        personal_color_similarity = self.l1_similarity_model(target_feature[type][AVERAGE_RGB], personal_color)

        final_similarity = last_activation_volume_similarity * self.alpha[0] + gram_matrix_similarity * self.alpha[1] + personal_color_similarity * self.alpha[3]
        final_similarity /= sum(self.alpha)

        return final_similarity


    def __call__(self, user_inputs, type, personal_color, k=5):
        user_features = [self.featuring_model(user_input) for user_input in user_inputs]

        similarity_result = {path:0.0 for path in self.recommended[type]}

        for user_feature in user_features:
            for target_input in self.recommended[type]:
                similarity_result[target_input] += self.getSimilarity(user_feature, target_input, type, torch.tensor(personal_color))

        return [k for k, v in sorted(similarity_result.items(), key=lambda item: item[1], reverse=True)][:k]







