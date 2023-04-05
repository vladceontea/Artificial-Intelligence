
import torch
import torch.nn as nn
from matplotlib import pyplot
from torch.autograd import Variable
from torch.optim import Adam
from torch.utils.data import DataLoader

from Task2 import ImageClassifierDataset
from constants import BATCH_SIZE, LEARNING_RATE, EPOCHS

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Unit(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(Unit, self).__init__()

        self.conv = nn.Conv2d(in_channels=in_channels, kernel_size=3, out_channels=out_channels, stride=1, padding=1)
        self.bn = nn.BatchNorm2d(num_features=out_channels)
        self.relu = nn.ReLU()

    def forward(self, input):
        output = self.conv(input)
        output = self.bn(output)
        output = self.relu(output)

        return output


class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()

        # Create 14 layers of the unit with max pooling in between
        self.unit1 = Unit(in_channels=3, out_channels=32)
        self.unit2 = Unit(in_channels=32, out_channels=32)
        self.unit3 = Unit(in_channels=32, out_channels=32)

        self.pool1 = nn.MaxPool2d(kernel_size=2)

        self.unit4 = Unit(in_channels=32, out_channels=64)
        self.unit5 = Unit(in_channels=64, out_channels=64)
        self.unit6 = Unit(in_channels=64, out_channels=64)
        self.unit7 = Unit(in_channels=64, out_channels=64)

        self.pool2 = nn.MaxPool2d(kernel_size=2)

        self.unit8 = Unit(in_channels=64, out_channels=128)
        self.unit9 = Unit(in_channels=128, out_channels=128)
        self.unit10 = Unit(in_channels=128, out_channels=128)
        self.unit11 = Unit(in_channels=128, out_channels=128)

        self.pool3 = nn.MaxPool2d(kernel_size=2)

        self.unit12 = Unit(in_channels=128, out_channels=128)
        self.unit13 = Unit(in_channels=128, out_channels=128)
        self.unit14 = Unit(in_channels=128, out_channels=128)

        self.avgpool = nn.AvgPool2d(kernel_size=4)

        # Add all the units into the Sequential layer in exact order
        self.net = nn.Sequential(self.unit1, self.unit2, self.unit3, self.pool1, self.unit4, self.unit5, self.unit6
                                 , self.unit7, self.pool2, self.unit8, self.unit9, self.unit10, self.unit11, self.pool3,
                                 self.unit12, self.unit13, self.unit14, self.avgpool)

        self.fc = nn.Linear(in_features=128, out_features=1)

    def forward(self, input):
        output = self.net(input)
        output = output.view(-1, 128)
        output = self.fc(output)
        output = torch.sigmoid(output)
        return output


def adjust_learning_rate(epoch):
    lr = 0.001

    if epoch > 45:
        lr = lr / 1000000
    elif epoch > 37:
        lr = lr / 100000
    elif epoch > 30:
        lr = lr / 10000
    elif epoch > 22:
        lr = lr / 1000
    elif epoch > 15:
        lr = lr / 100
    elif epoch > 7:
        lr = lr / 10

    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


def save_models(epoch):
    torch.save(model.state_dict(), f"models/network_epoch_{epoch}")
    print("Checkpoint saved")


def test():
    model.eval()
    test_accuracy = 0.0
    test_loss = 0.0
    for i, (images, labels) in enumerate(test_loader):
        if cuda_avail:
            images = Variable(images.cuda())
            labels = Variable(labels.cuda())
        outputs = model(images)
        prediction = torch.round(outputs.data)
        loss = loss_fn(outputs, labels)
        test_loss += loss.cpu().data.item() * images.size(0)
        test_accuracy += torch.sum(torch.eq(prediction, labels.data))

    test_accuracy = test_accuracy / test_set_size
    test_loss = test_loss / test_set_size

    return test_accuracy, test_loss


def train(epochs):
    acc = []
    best_acc = 0
    print("Training Started...")
    for epoch in range(epochs):

        model.train()
        train_acc = 0.0
        train_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            if cuda_avail:
                images = Variable(images.cuda())
                labels = Variable(labels.cuda())

            optimizer.zero_grad()
            outputs = model(images)

            loss = loss_fn(outputs, labels)

            loss.backward()

            optimizer.step()

            train_loss += loss.cpu().data.item() * images.size(0)

            prediction = torch.round(outputs.data)

            train_acc += torch.sum(torch.eq(prediction, labels.data))

        adjust_learning_rate(epoch)

        train_acc /= train_set_size
        train_loss /= train_set_size

        test_acc, test_loss = test()

        if test_acc > best_acc:
            save_models(epoch)
            best_acc = test_acc

        print(f"Epoch {epoch}, Train Accuracy: {train_acc} , TrainLoss: {train_loss} , Test Accuracy: {test_acc}, Test Loss: {test_loss}")
        acc.append(test_acc)

    pyplot.plot(acc)
    pyplot.show()


if __name__ == '__main__':
    # create the dataset
    dataset = ImageClassifierDataset()
    dataset.load_images()
    train_set, test_set = dataset.split()
    train_set_size = len(train_set)
    test_set_size = len(test_set)

    # Create a loader for the training set and testing set
    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=False, num_workers=4)
    # Check if gpu support is available
    cuda_avail = torch.cuda.is_available()

    # Create model, optimizer and loss function
    model = SimpleNet()
    if cuda_avail:
        model.cuda()
    optimizer = Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=0.0001)
    loss_fn = nn.BCELoss()
    train(EPOCHS)