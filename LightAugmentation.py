import random
import numpy as np
import skimage.draw as draw
from scipy.ndimage import distance_transform_edt as dt
import cv2
import matplotlib.pyplot as plt
import json
import os
class Illumination:

    def __init__(self, local_mask=(80, 100), global_mask=(30, 40),
                 flip_and_noise=False, augmenting_prob=1):

        self.augmenting_prob = augmenting_prob
        self.local_mask = local_mask
        self.global_mask = global_mask
        self.flip_and_noise = flip_and_noise
        self.augment_illumination = any(x > 0 for x in list(local_mask) + list(global_mask))

    def get_mask(self, img, minmax=(80, 100), colored = False):
        mask = np.zeros_like(img[..., 0])
        x, y = mask.shape
        min_dim = min(x, y)
        if np.random.random() > 0.5:  # Circle-shaped masks
            random_r = np.random.randint(int(min_dim / 3), int(min_dim / 2))
            random_r = int(random_r / 2)
            random_x = np.random.randint(random_r, x - random_r)
            random_y = np.random.randint(random_r, y - random_r)
            rr, cc = draw.circle(random_x, random_y, random_r)
        else:  # Ellipse-shaped masks
            random_r = np.random.randint(int(min_dim / 3), int(min_dim / 2))
            random_r = int(random_r / 2)
            random_x = np.random.randint(random_r, x - random_r)
            random_y = np.random.randint(random_r, y - random_r)
            rr, cc = draw.ellipse(random_x, random_y, random_r,
                                  random_r * np.random.uniform(low=random_r, high=0.8, size=1)[0],
                                  shape=(x, y), rotation=np.random.random() * np.pi * 2 - np.pi)
        mask[rr, cc] = 1

        if colored:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            rgb = [r, g, b]
            mask = dt(mask)
            rv = np.random.randint(minmax[0], minmax[1])
            mask = mask / np.max(mask) * rv
            mask = np.stack((mask,) * 3, axis=-1)
            mask = mask * (np.array(rgb) / 255)
        else:
            mask = dt(mask)
            rv = np.random.randint(minmax[0], minmax[1])
            mask = mask / np.max(mask) * rv
            mask = np.stack((mask,) * 3, axis=-1)

        return mask, rv

    def illumination_augmenter(self, img, colored, global_mask=(30, 40), local_mask=(80, 100)):
        img = np.squeeze(img)
        # Only local changes
        if any(x > 0 for x in local_mask):
            mask, ch = self.get_mask(img, local_mask, colored)
            sign = '-'
            if np.random.random() > 0.5:
                sign = '+'
                img = img + mask
            else:
                img = img - mask
            # Local and global changes
            if any(x > 0 for x in global_mask):
                if np.random.random() > 0.5:
                    sign += '+'
                else:
                    sign += '-'
                if sign == '--' or sign == '++':
                    global_max = global_mask[1]
                    global_min = global_mask[0]
                else:
                    global_max = global_mask[1] + ch
                    global_min = global_mask[0] + ch

                if sign[1] == '+':
                    img = img + np.ones_like(img) * np.random.randint(global_min, global_max)
                elif sign[1] == '-':
                    img = img + np.ones_like(img) * np.random.randint(global_min, global_max) * -1
        return img[np.newaxis, ...]

def visualize(image):

    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

def generate_Image(img:bytes, colored: bool = False):
    #img = cv2.imdecode(np.frombuffer(image, np.uint8), 1)
    illum = Illumination()
    if colored:
        newImage = illum.illumination_augmenter(img, colored = True)
    else:
        newImage = illum.illumination_augmenter(img, colored = False)

    newImage = np.squeeze(newImage, 0)

    return newImage

def augment_data(files_directory,destination_directory):

    imagePaths = os.listdir(files_directory + '/images/')
    i=len(os.listdir(destination_directory + '/images/')) +1
    for imagePath in imagePaths:

        image = cv2.imread(files_directory + '/images/' +imagePath)
        cv2.imwrite(destination_directory + '/images/' + str(i) + '.jpg', generate_Image(image))

        image_corresponding_label = imagePath.split('.')[-2] + ".json"

        obj = json.load(open(files_directory + '/labels/json/' + image_corresponding_label))
        open(destination_directory + '/labels/json/'+ str(i) +'.json', "w").write(
            json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
        )
        i=i+1

'''imagepath='datasets/data/images/2.jpg'
image = cv2.imread(imagepath)
cv2.imwrite('hello.jpg', generate_Image(image))'''

augment_data('/home/youssef/Desktop/Training_Dataset30k/DR2(30k)','/home/youssef/Desktop/Training_Dataset30k/DR2_LightAug(30k)')