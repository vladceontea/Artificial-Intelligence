# create a thumbnail of an image
from PIL import Image
# load the image
image = Image.open('f1.jpg')
# report the size of the image
print(image.size)
# create a thumbnail and preserve aspect ratio
image.thumbnail((100,100))
# report the size of the thumbnail
print(image.size)