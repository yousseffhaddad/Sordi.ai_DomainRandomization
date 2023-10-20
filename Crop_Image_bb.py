import os
import json
import random
import cv2
import albumentations as A

labels_path = '/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/SythnethicPoC_100%[7k]/labels/json/'
labels = os.listdir(labels_path)

# Specify the directory to save cropped images
output_directory = '/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/SythnethicPoC_100%[7k]/cropped_Images/'
os.makedirs(output_directory, exist_ok=True)

# Define the size for cropping and resizing (512x512)
crop_size = 512

for item in labels:
    # Load the JSON file
    json_file_path = os.path.join(labels_path, item)
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    for i, obj in enumerate(data):
        # Extract bounding box coordinates
        Left = int(obj["Left"])
        Top = int(obj["Top"])
        Right = int(obj["Right"])
        Bottom = int(obj["Bottom"])

        image_path = '/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/SythnethicPoC_100%[7k]/images/' + item.split('.')[-2] + '.jpg'
        image = cv2.imread(image_path)

        # Define the augmentation pipeline
        transform = A.Compose([
            A.Crop(x_min=Left, y_min=Top, x_max=Right, y_max=Bottom),
            A.Resize(crop_size, crop_size)
        ], p=1)

        transformed = transform(image=image)
        cropped_resized_image = transformed['image']

        # Save the cropped and resized image
        image_name = item.split('.')[-2] + '__' + str(i) + '.jpg'
        cropped_image_path = os.path.join(output_directory, image_name)
        cv2.imwrite(cropped_image_path, cropped_resized_image)
