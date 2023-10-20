import os
import json
import cv2
import matplotlib.pyplot as plt

def checkAssets_bb(files_directory):

    json_path = files_directory + "/labels/json/"
    labels_list = os.listdir(json_path)
    for file in labels_list:
        with open(json_path +file,'r') as f:
            json_file = json.load(f)
        i=0
       # min=100000
        for json_data in json_file:
            width = abs(json_data['Left'] - json_data['Right'])
            height = abs(json_data['Top'] - json_data['Bottom'])
            threshold=width*height
            print(file,i,json_data['ObjectClassName'],threshold)
            i=i+1

        #print(min)

def cleaning_bb(files_directory):
    json_path = files_directory + "/labels/json/"
    labels_list = os.listdir(json_path)
    print(labels_list)
    #for Eval 5
    #assets_threshold = {"klt_box": 5000, "stillage": 9800, "fire_extinguisher": 700, "pallet": 66000, "jack": 20000, "dolly": 5800}
    #for Eval6
    #assets_threshold = {"klt_box": 10000, "stillage": 9800, "fire_extinguisher": 8000, "pallet": 66000, "jack": 20000,"dolly": 5800}
    assets_threshold = {"stillage":7000,"dolly": 5000}
    ct=0
    for label in labels_list:
        new_json = {}
        j = 0
        with open(files_directory + "/labels/json/" + label, 'r') as f:
            json_file = json.load(f)

        for json_data in json_file:
            width = abs(json_data['Left'] - json_data['Right'])
            height = abs(json_data['Top'] - json_data['Bottom'])
            threshold=width*height
            if threshold > assets_threshold[json_data['ObjectClassName']] :
                new_json[j] = json_data
                j += 1

        final_json_version = [val for key, val in new_json.items()]

        # Output the updated file with pretty JSON
        open(files_directory + '/labels/json/' + label, "w").write(
            json.dumps(final_json_version, sort_keys=False, indent=4, separators=(',', ': ')))

def drawBox(boxes,image,image_name):
    for i in range(0, len(boxes)):
        # changed color and width to make it visible
        if boxes[i][4] =="Klt_box":
            color=(255, 0, 0)
        elif boxes[i][4]=="fire_extinguisher":
            color=(255, 255, 0)
        elif boxes[i][4]=="pallet":
            color=(0, 0, 255)
        elif boxes[i][4]=="dolly":
            color=(0, 255, 0)
        # changed color and width to make it visible
        cv2.rectangle(image, (boxes[i][0], boxes[i][1]), (boxes[i][2], boxes[i][3]),color, 4)
        name = boxes[i][4]
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        font_color = (0, 0, 0)  # White color for the text (BGR format)
        text_position = (boxes[i][0], boxes[i][1] - 10)  # Position of the text
        cv2.putText(image, name, text_position, font, font_scale, font_color,thickness , cv2.LINE_AA)
    cv2.imwrite('/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/StableDiffusion_100%[7k]_WithBoundingBoxes/'+image_name,image)
    #cv2.rectangle(image, (boxes[0], boxes[1]), (boxes[2], boxes[3]), (255, 0, 0),2)
    #plt.figure(figsize=(10, 10))
    #plt.axis('off')
    #plt.imshow(image)
    #plt.show()

#Calling functions

'''def drawBox_allImages(files_directory):
    images_path = files_directory + "/images/"
    images_list = os.listdir(images_path)
    print(images_list)
    for img in images_list:
        image = cv2.imread(files_directory + "/images/" +img)
        image_corresponding_label = img.split('.')[-2] + ".png.json"
        print(image_corresponding_label)
        image_label = json.load(open(files_directory + "/labels/json/" + image_corresponding_label))
        bboxes=[]
        for i in range(len(image_label[["bounding-boxes"]])):
            print(i)
            origLeft = int(image_label[i]["coordinates"]["Left"])
            origTop = int(image_label[i]["coordinates"]["Top"])
            origRight = int(image_label[i]["coordinates"]["Right"])
            origBottom = int(image_label[i]["coordinates"]["Bottom"])
            #print(origBottom,origTop,origRight,origLeft)
            bboxes.append([origLeft, origTop, origRight, origBottom])
            print(bboxes)

        drawBox(bboxes,image)'''

def drawBox_allImages(files_directory):
    images_path = files_directory + "/images/"
    images_list = os.listdir(images_path)
    print(images_list)
    for img in images_list:
        image = cv2.imread(files_directory + "/images/" +img)
        image_corresponding_label = img.split('.')[-2] + ".json"
        print(image_corresponding_label)
        image_label = json.load(open(files_directory + "/labels/json/" + image_corresponding_label))
        bboxes=[]
        for i in range(len(image_label)):
            print(i)
            origLeft = int(image_label[i]["Left"])
            origTop = int(image_label[i]["Top"])
            origRight = int(image_label[i]["Right"])
            origBottom = int(image_label[i]["Bottom"])
            objectclassname=str(image_label[i]["ObjectClassName"])
            #print(origBottom,origTop,origRight,origLeft)
            bboxes.append([origLeft, origTop, origRight, origBottom,objectclassname])
            print(bboxes)

        drawBox(bboxes,image,img)


#cleaning_bb('/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/Exp3_evaluation_Regensburg(After_cleaning)')
#checkAssets_bb('/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/evaluation_Exp3_Munich')
drawBox_allImages('/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/StableDiffusion_100%[7k]')
#/home/youssef/Desktop/Sordi_Samples/scene2_large+small
