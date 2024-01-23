import torch
import torchvision
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
from torchvision.transforms.functional import to_pil_image, crop
import torch.nn as nn
from typing import *

class SimilarityModel:
    def __init__(self, x):