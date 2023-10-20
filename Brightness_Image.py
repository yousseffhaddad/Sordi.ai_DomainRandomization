
import os
import cv2
import numpy as np
images=os.listdir("/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/evaluation_Exp3_Munich/images/")
for img in images :
    # Load the image
    image_path = '/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/evaluation_Exp3_Munich/images/'+img
    image = cv2.imread(image_path)

    # Convert the image to the LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Split the LAB image into L, A, and B channels
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Increase brightness of the L (black) channel
    brightness_increase = 50
    adjusted_l_channel = cv2.add(l_channel, brightness_increase)

    # Combine the adjusted L channel with the original A and B channels
    adjusted_lab_image = cv2.merge((adjusted_l_channel, a_channel, b_channel))

    # Convert the adjusted LAB image back to BGR color space
    adjusted_bgr_image = cv2.cvtColor(adjusted_lab_image, cv2.COLOR_LAB2BGR)

    cv2.imwrite('/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/evaluation_Exp3_Munich/images/'+img, adjusted_bgr_image)