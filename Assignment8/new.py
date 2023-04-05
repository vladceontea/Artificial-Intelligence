from Task2 import ImageClassifierDataset

dataset = ImageClassifierDataset()
dataset.load_images()
train_set, test_set = dataset.split()

print(train_set.labels)
print(dataset.labels)