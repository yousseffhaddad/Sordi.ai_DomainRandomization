from PIL import Image
import os
import sys

#arg1 = sys.argv[1]
#arg2 = sys.argv[2]
arg1="/home/youssef/Desktop/GenAI_Images/pallet[6k]/images/"
arg2="/home/youssef/Desktop/GenAI_Images/pallet[6k]/images_jpg/"
images = os.listdir(arg1)
print("processing ...")
images_dest = os.listdir(arg2)
for img in images:
    if img.split('.')[-2] + ".jpg" not in images_dest:
        print(img)
        save_img = img.split('.')[-2] + ".jpg"
        image = Image.open(arg1 + '/' + img)
        image = image.convert('RGB')
        image.save(arg2 + '/' + save_img, 'JPEG')


