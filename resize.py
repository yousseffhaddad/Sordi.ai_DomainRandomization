import os
import sys
import cv2

files_directory='/home/youssef/Desktop/Real_Images/Real_Images_8categories/Klt_box_Real/images'
images = os.listdir(files_directory)
new_size = (512, 512)
for img in images:

    if img.split('.')[1] != 'txt':
        image = cv2.imread(files_directory + '/' + img)
        # Set the desired new size

        # Resize the image
        resized_image = cv2.resize(image, new_size)

        # Save the resized image
        cv2.imwrite(files_directory + '/' + img, resized_image)