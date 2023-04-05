
from torchvision import transforms

import torch
from PIL import Image

from network import SimpleNet

network = SimpleNet()
network.load_state_dict(torch.load("models/network_epoch_11"))
network.eval()
label_to_class = {1: 'FACE', 0: 'NOT FACE'}

transforms = transforms.Compose([
    transforms.Resize(32),
    transforms.CenterCrop(32),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

def test_image():
    while True:
        try:
            filename = input('Filename: ')
            file = f'TestDatabase/{filename}'
            image = transforms(Image.open(file))
            image = image.unsqueeze(0)
            output = network(image)
            if output.data[0] > 0.95:
                print("FACE")
            else:
                print("NOT FACE")
            print(output.data[0])
        except Exception as e:
            print(e)


test_image()

