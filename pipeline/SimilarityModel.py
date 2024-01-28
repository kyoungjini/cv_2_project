import torch
import torchvision
from PIL import Image
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
from torchvision.transforms.functional import to_pil_image, crop
import torch.nn as nn
from typing import *

from pipeline.FeaturingModel import FeaturingModel

PERSONAL_COLOR_TABLE = {

}

class SimilarityModel:
    def __init__(self, recommended, featuring_model: FeaturingModel):
        """
        유사도를 계산하여 추천 랭킹을 받는 클래스의 생성자입니다.


        :param recommended: 상의, 하의에 대한 정보와 각 옷의 특징 파일 경로
                            예를 들어, recommended = {"상의":["./pipeline/features/feature0.pt", "./pipeline/features/feature1.pt"], "하의":["./pipeline/features/feature2.pt"]}
        :param featuring_model: 유저의 입력 사진에 대해 특징 추출하는 모델.
        """
        self.recommended = recommended
        self.featuring_model = featuring_model

        self.cosine_similarity_model = torch.nn.CosineSimilarity()
        self.l1_similarity_model = lambda x, y : 1/(F.l1_loss(x, y) + 1e-8)

    def getPersonalColor(self, user_input_features):
        average_rgb = user_input_features[0]["average_rgb"]
        for feature in user_input_features[1:]:
            average_rgb += feature["average_rgb"]
        average_rgb /= len(user_input_features)




