import os
import random

import numpy as np
import torch

from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

from constants import *

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class ImageClassifierDataset(Dataset):
    def __init__(self, image_classes=CLASSES):
        self.images = []
        self.labels = []
        self.classes = list(set(image_classes))
        self.class_to_label = {c: float(i) for i, c in enumerate(self.classes)}
        self.image_size = 32
        self.transforms = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.CenterCrop(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def class_images(self, image_list, image_classes):
        for image, image_class in zip(image_list, image_classes):

            transformed_image = self.transforms(image)
            self.images.append(transformed_image)

            label = self.class_to_label[image_class]
            self.labels.append(label)

    def load_images(self):
        images = []
        for directory in os.listdir('FaceDatabase'):
            images.clear()
            print(f'Loading {directory} images')
            folder_images = [file_name for file_name in os.listdir(f'FaceDatabase/{directory}')]
            np.random.shuffle(folder_images)

            for image in folder_images:
                picture = Image.open(f'FaceDatabase/{directory}/{image}')
                images.append(picture)

            if directory == 'Other':
                self.class_images(images, ['NOT FACE' for _ in images])
            else:
                self.class_images(images, ['FACE' for _ in images])

    def split(self):
        images_labels = list(zip(self.images, self.labels))
        np.random.shuffle(images_labels)
        data = list(range(len(images_labels)))
        train_data = []
        test_data = []
        for image in data:
            if random.random() < 0.8:
                train_data.append(image)
            else:
                test_data.append(image)

        train_set = ImageClassifierDataset()
        train_set.images = torch.tensor([])
        train_set.labels = torch.tensor([])
        train_set.images = [images_labels[i][0] for i in train_data]
        train_set.labels = [images_labels[i][1] for i in train_data]

        train_set.images = torch.stack(train_set.images)

        test_set = ImageClassifierDataset()
        test_set.images = torch.tensor([])
        test_set.labels = torch.tensor([])
        test_set.images = [images_labels[i][0] for i in test_data]
        test_set.labels = [images_labels[i][1] for i in test_data]

        test_set.images = torch.stack(test_set.images)

        return train_set, test_set

    def __getitem__(self, index):
        return self.images[index], self.labels[index]

    def __len__(self):
        return len(self.images)