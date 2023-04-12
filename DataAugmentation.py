import albumentations as A
import cv2
import matplotlib.pyplot as plt
import random
import os
import json

def visualize(image):

    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

def transform (imagepath) :

    #Declare an augmentation pipeline
    choices=[A.RGBShift(r_shift_limit=20, g_shift_limit=20, b_shift_limit=20, always_apply=False, p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, always_apply=False, p=0.5),
        A.CLAHE (clip_limit=4.0, tile_grid_size=(8, 8), always_apply=False, p=0.5),
        A.ChannelShuffle(p=0.5)]


    num_items_to_select = random.randint(0,5)
    probabilties=[0.2,0.2,0.2,0.2,0.2]

    selected_items=random.choices(choices,probabilties,k=num_items_to_select)

    transform = A.Compose(selected_items)

    # Read an image with OpenCV and convert it to the RGB colorspace
    image = cv2.imread(imagepath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Augment an image
    transformed = transform(image=image)
    transformed_image = transformed["image"]

    return transformed_image

def augment_data(files_directory,destination_directory):

    imagePaths = os.listdir(files_directory + '/images/')
    i=len(os.listdir(destination_directory + '/images/')) +1
    for imagePath in imagePaths:

        image = transform(files_directory + '/images/'+imagePath)
        cv2.imwrite(destination_directory + '/images/' + str(i) + '.jpg', image)

        image_corresponding_label = imagePath.split('.')[-2] + ".json"

        obj = json.load(open(files_directory + '/labels/json/' + image_corresponding_label))
        open(destination_directory + '/labels/json/'+ str(i) +'.json', "w").write(
            json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
        )
        i=i+1
