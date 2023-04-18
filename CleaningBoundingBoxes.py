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
    assets_threshold = {"klt_box": 10000, "stillage": 9800, "fire_extinguisher": 8000, "pallet": 66000, "jack": 20000,"dolly": 5800}
    for label in labels_list:
        new_json = {}
        j = 0
        with open(files_directory + "/labels/json/" + label, 'r') as f:
            json_file = json.load(f)

        for json_data in json_file:
            width = abs(json_data['Left'] - json_data['Right'])
            height = abs(json_data['Top'] - json_data['Bottom'])
            threshold=width*height
            if threshold >= assets_threshold[json_data['ObjectClassName']] :
                new_json[j] = json_data
                j += 1

        final_json_version = [val for key, val in new_json.items()]

        # Output the updated file with pretty JSON
        open(files_directory + '/labels/json/' + label, "w").write(
            json.dumps(final_json_version, sort_keys=False, indent=4, separators=(',', ': '))

        )
def drawBox(boxes,image):
    for i in range(0, len(boxes)):
        # changed color and width to make it visible
        cv2.rectangle(image, (boxes[i][0], boxes[i][1]), (boxes[i][2], boxes[i][3]), (255, 0, 0), 1)
    #cv2.rectangle(image, (boxes[0], boxes[1]), (boxes[2], boxes[3]), (255, 0, 0),2)
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

#Calling functions

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
            #print(origBottom,origTop,origRight,origLeft)
            bboxes.append([origLeft, origTop, origRight, origBottom])
            print(bboxes)

        drawBox(bboxes,image)


#cleaning_bb('/home/youssef/Desktop/Sordi.ai_Dataset/Spartunburg')
#checkAssets_bb('datasets/data/')
drawBox_allImages('/home/youssef/Desktop/Training_Dataset30k/FollowPath_Regensburg')