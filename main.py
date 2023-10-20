import os
import json
import matplotlib.pyplot as plt
import cv2
import random

import PreProcessing
import PreProcessing as pp
import DataAugmentation as da
import numpy as np

def check_percentage_histogram (files_directory,assets):

    print ('checking')
    percentages=[]

    for asset in assets :

        asset_count=0
        for json_File in os.listdir(files_directory+"/labels/json/") :

            labels=[]
            obj=json.load(open(files_directory + '/labels/json/' + json_File))
            for i in range (len(obj)):

                labels.append(obj[i]['ObjectClassName'])
            if  labels.count(asset)>0:
                asset_count=asset_count+1

        asset_percentage=(asset_count *100 )/len(os.listdir(files_directory + '/labels/json/'))
        percentages.append(asset_percentage)
        print(asset_percentage,'%')

    plt.bar(assets,percentages)

    plt.xlabel('Assets')

    plt.ylabel('Percentage')

    plt.title('Assets Distribution')

    plt.show()

def check_percentage(files_directory,selected_items,assets):

    asset_percentage_dic = {'dolly':0, 'Klt_box':0, 'pallet':0, 'fire_extinguisher':0}
    if len(selected_items) != 0 :
        for asset in assets:

            asset_count = 0
            for json_File in selected_items:

                labels = []
                obj = json.load(open(files_directory + '/labels/json/' + json_File))
                for i in range(len(obj)):
                    labels.append(obj[i]['ObjectClassName'])
                if labels.count(asset) > 0:
                    asset_count = asset_count + 1

            asset_percentage = (asset_count * 100) / len(selected_items)
            asset_percentage_dic[asset] = asset_percentage

    min_key = min(asset_percentage_dic, key=asset_percentage_dic.get)
    return min_key


def transfer_data (source_directory,destination_directory,nb_of_images):
    original_Images=os.listdir("/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/SythnethicPoC_100%[7k]/labels/json/")
    #data = json.load(open(source_directory + '/objectclasses.json'))
    assets_needed = ['dolly', 'Klt_box', 'pallet', 'fire_extinguisher']
    if nb_of_images <= len(os.listdir(source_directory + '/labels/json/')) :

        #open(destination_directory + '/objectclasses.json', "w").write(
          #  json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
        #)

        labels = os.listdir(source_directory + '/labels/json/')
        i=len(os.listdir(destination_directory + '/labels/json/')) +1

        #print(i)
        #random_items = random.sample(labels, nb_of_images)
        random_items = random.sample(labels,len(os.listdir(source_directory + '/labels/json/')))
        selected_items=[]
        ct=0
        for item in random_items :
            if ct>=nb_of_images:
                break
            obj = json.load(open(source_directory + '/labels/json/' + item))
            if ct%50==0 :
                asset=check_percentage(source_directory,selected_items,assets_needed)
                print(asset)
            objectclass_name=[]
            for j in range (len(obj)):
                objectclass_name.append(obj[j]['ObjectClassName'])

            objectclass_name_set = list(set(objectclass_name))

            if len(objectclass_name_set)<=1 and len(objectclass_name)<=1 and asset in objectclass_name and item not in original_Images:
                selected_items.append(item)
                random_items.remove(item)
                ct = ct + 1
                print(ct)

        print(len(selected_items))
        if len(selected_items)<nb_of_images:
            random_items = random.sample(random_items, nb_of_images - len(selected_items)) + selected_items
        else:
            random_items=selected_items
        print(len(random_items))
        for label in random_items :
            l=label.split('.')
            label_corresponding_image = l[-2] + ".jpg"
            image = cv2.imread(source_directory + '/images/' + label_corresponding_image)
            cv2.imwrite(destination_directory + '/images/' + l[-2] + '.jpg', image)
            obj = json.load(open(source_directory + '/labels/json/' + label))
            open(destination_directory + '/labels/json/'+ l[-2] +'.json', "w").write(
                json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
            )
            i=i+1

    else :
        print ("your nb of images that you provided exceed the capacity ")

'''def transfer_regen(source_directory,destination_directory):

    json_path = source_directory + "/labels/json/"
    labels_list = os.listdir(json_path)
    #assets_threshold = {"dolly": 13000, "stillage": 18000, "str": 24000}
    #assets_threshold = {"dolly": 20000, "stillage": 25000, "str": 26000}
    assets_threshold = {"dolly": 30000, "stillage": 30000, "str": 30000}
    selected_items = []
    counter=0
    i=0
    ct=0
    for label in labels_list:
        flag1 = True
        flag2=False
        if counter == 200 :
            break
        if ct % 20 == 0:
            asset = check_percentage(source_directory, selected_items, assets_needed)
            print(asset)
        with open(source_directory + "/labels/json/" + label, 'r') as f:
            json_file = json.load(f)

        for json_data in json_file:
            if json_data['ObjectClassName'] == asset:
                flag2=True
                width = abs(json_data['Left'] - json_data['Right'])
                height = abs(json_data['Top'] - json_data['Bottom'])
                threshold=width*height
                if threshold < assets_threshold[json_data['ObjectClassName']] :
                    flag1=False
                    break
        if flag1 and flag2 :
            selected_items.append(label)
            counter=counter +1

    for label in selected_items:
        label_corresponding_image = label.split('.')[-2] + ".png"
        image = cv2.imread(source_directory + '/images/' + label_corresponding_image)
        cv2.imwrite(destination_directory + '/images/' + str(i) + '.png', image)
        obj = json.load(open(source_directory + '/labels/json/' + label))
        open(destination_directory + '/labels/json/' + str(i) + '.json', "w").write(
            json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
        )
        i=i+1'''



def transfer_data_genAI(source_directory,destination_directory,nbofimages):

        items = os.listdir(source_directory+"images/")
        i = int(len(os.listdir(destination_directory+"images/")))+1
        #i=int(len(os.listdir(destination_directory))/2 +1)
        #j = int(len(os.listdir(destination_directory))/2 + 1)

        print("I IS :",i)

        ct=0
        for item in items :
            if ct>=nbofimages:
                break
            if item.split('.')[-1] == 'jpg':
                label_corresponding_image = item.split('.')[-2]+ ".json"
                image = cv2.imread(source_directory +"images/"+ item)
                cv2.imwrite(destination_directory+"images/" + item.split('.')[-2] + '_Synth'+str(i)+'.jpg', image)
                obj = json.load(open(source_directory + 'labels/json/' + label_corresponding_image))
                open(destination_directory + 'labels/json/' + item.split('.')[-2] + '_Synth'+str(i)+'.json', "w").write(
                    json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
                )
                ct=ct+1
                i=i+1
            '''else :
                print("hello")
                with open(source_directory + item, "r") as file:
                    # Read the content of the file
                    content = file.read()
                file = open(destination_directory + str(j) + '.txt', 'w')

                file.write(content)
                j=j+1'''

def delete (files_directory : str,nb):
  j=0
  for filename in os.listdir(files_directory + '/labels/json/'):
    data = json.load(open(files_directory + '/labels/json/' + filename))
    for i in range (len(data)):
        if  data[i]['ObjectClassName']=='dolly':
          label_corresponding_image = filename.split('.')[-2] + ".jpg"
          os.remove(files_directory + '/labels/json/' + filename)
          os.remove(files_directory + '/images/' + label_corresponding_image)
          print(f"File {filename} has been deleted")
          j=j+1
          break
    if j>=nb:
        break

'''def drawBox(boxes,image):

    cv2.rectangle(image, (boxes[0], boxes[1]), (boxes[2], boxes[3]), (255, 0, 0),2)
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()'''

#Calling functions

def adjust_labels(directory):
    labels = os.listdir(directory + "/labels/json/")
    ct=0
    for l in labels:
        label = json.load(open(directory + "/labels/json/" + l))
        bounding_boxes = label["bounding-boxes"]
        transformed_data = []
        for i in range(len(bounding_boxes)):
            transformed_item = {
                "Id": ct,
                "ObjectClassName": bounding_boxes[i]["ObjectClassName"],
                "Left": bounding_boxes[i]["coordinates"]["left"],
                "Top": bounding_boxes[i]["coordinates"]["top"],
                "Right": bounding_boxes[i]["coordinates"]["right"],
                "Bottom": bounding_boxes[i]["coordinates"]["bottom"],
                "Confidence":bounding_boxes[i]["confidence"]
            }
            transformed_data.append(transformed_item)
            ct=ct+1
        with open(directory + "/labels/json/"+l, 'w') as json_file:
            json.dump(transformed_data, json_file, indent=4)
def drawBox(boxes,image):
    for i in range(0, len(boxes)):
        # changed color and width to make it visible
        if boxes[i][4] =="Klt_box":
            color=(255, 0, 0)
        elif boxes[i][4]=="jack":
            color=(255, 255, 0)
        elif boxes[i][4]=="pallet":
            color=(0, 0, 255)
        elif boxes[i][4]=="dolly":
            color=(0, 255, 0)
        cv2.rectangle(image, (boxes[i][0], boxes[i][1]), (boxes[i][2], boxes[i][3]), color, 2)
        name = boxes[i][4]
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        font_color = (0, 0, 0)  # White color for the text (BGR format)
        text_position = (boxes[i][0], boxes[i][1] - 10)  # Position of the text
        cv2.putText(image, name, text_position, font, font_scale, font_color,thickness , cv2.LINE_AA)
    #cv2.imwrite('/home/youssef/Desktop/Images_Marc/GenAi_Images_export_230816084556/GenAi_Images_export_230816084556/images_booundingBoxes/7.jpg', image)
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

'''image = cv2.imread('/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Real_100%[7k]/images/333_Real5.jpg')
image_label = json.load(open('/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Real_100%[7k]/labels/json/333_Real5.jpg.json'))
bboxes=[]
for i in range (len(image_label)):
    origLeft = int(image_label[i]["Left"])
    origTop = int(image_label[i]["Top"])
    origRight = int(image_label[i]["Right"])
    origBottom = int(image_label[i]["Bottom"])
    bboxes.append([origLeft, origTop, origRight, origBottom,image_label[i]['ObjectClassName']])

drawBox(bboxes,image)'''

def transfer (files_directory,destination_directory):
    labels=os.listdir(files_directory+"/labels/json/")
    assets=[]
    for label in labels :
        assets=[]
        obj = json.load(open(files_directory + '/labels/json/' + label))
        for o in obj:
            assets.append(o["ObjectClassName"])
        if "pallet" in assets and "dolly" in assets :
            l=label.split('.')
            label_corresponding_image = l[-2] + ".jpg"
            image = cv2.imread(files_directory + '/images/' + label_corresponding_image)
            cv2.imwrite(destination_directory + l[-2] + '.jpg', image)
            print(label)

#transfer("/home/youssef/Desktop/Sordi_poc/Sordi_poc_10k_20230825125301","/home/youssef/Desktop/Style_Gan[Cond_Images]/pallet,dolly/")

#assets_needed=["klt_box","stillage","fire_extinguisher","pallet","jack","dolly"]
assets_needed=["dolly", "Klt_box", "fire_extinguisher","pallet"]
#print(check_percentage('/home/youssef/Desktop/Sordi.ai_Dataset/Sordi_POC',assets_needed))

#pp.remove_duplicates_using_hash('/home/youssef/Desktop/Training_Dataset(15k)/Reg_rand+fllwpath70%')
#pp.change_subassets_names('/home/youssef/Desktop/Real_Images/FLLWpath_Real_Eval')
#pp.delete_uneeded_assets('/home/youssef/Desktop/Sordi_poc/Sordi_poc')
#pp.delete_empty_files('/home/youssef/Desktop/Sordi_poc/Sordi_poc')
#pp.add_object_class_id('/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp3/Real[7k]+SyntheticPoC[7k]')
#pp.delete_json("/home/youssef/Desktop/Real_Images/Eval_GenAIExperiments")
#pp.delete_empty_files('/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/Exp3_evaluation_Regensburg(After_cleaning)')


#pp.delete_json('/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/Synth_PoC100%[7k]_resized')
#pp.delete_images('/home/youssef/Desktop/Real_Images/FllwPath_Real')
#da.augment_data('/home/youssef/Desktop/Training_Dataset30k/DR2(30k)','/home/youssef/Desktop/Training_Dataset30k/DR2_Aug(30k)')
#print(len(os.listdir('/home/youssef/Desktop/Training_Dataset(15k)/Reg_fllwpath100%/images')))
#print(len(os.listdir('/home/youssef/Desktop/Training_Dataset(15k)/Reg_fllwpath100%/labels/json')))
#transfer_data('/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath_Synthetic/Sordi4/output3/resized6/Viewport','/home/youssef/Desktop/Training_Dataset(15k)/Reg_fllwpath100%',420)
#check_percentage_histogram('/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp2/Real50%+Diffusion50%[7k]',assets_needed)

#delete('/home/youssef/Desktop/Training_Dataset(15k)/FllwPath_regen100%',1939)
#/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath_Synthetic/Sordi2/output1/resized/Viewport jpg
#/home/youssef/Desktop/Sordi.ai_Dataset/regensburg_plant_720p  jpg
#/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath_Real png


#transfer_regen('/home/youssef/Desktop/Sordi.ai_Dataset/STR_export_230419074900','/home/youssef/Desktop/Evaluation_Dataset/Exp3_Eval')

#transfer_data('/home/youssef/Desktop/Sordi_poc/Sordi_poc','/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/SythnethicPoC_100%_1',300)

#pp.delete_json("/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/sordi_datasets/FllwPath_Synthetic/Sordi2/output2/resized2/Viewport")

#=================================================================================================================================================================================

#transfer_data_genAI("/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/StableDiffusion_100%[7k]/","/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp2/SynthPoC50%+Diffusion50%[7k]/",3500)
#adjust_labels("/home/youssef/Desktop/GenAI_Images/pallet[6k]/")
#pp.add_object_class_id("/home/youssef/Desktop/GenAI50%_Real50%_10k/")

#pp.delete_uneeded_assets('/home/youssef/Desktop/Sordi_poc/Sordi_poc_10k')
#pp.delete_empty_files('/home/youssef/Desktop/GenAI_Images/pallet[6k]')
#pp.delete_images_one_label('/home/youssef/Desktop/GenAI_Images/multiple_dollies[6k]')

#pp.delete_images_not_exist("/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/StableDiffusion_100%[7k]","/home/youssef/Desktop/SordiGenAI_Experiments_Datasets/Exp1/StableDiffusion_100%[7k]_WithBoundingBoxes")

#pp.transferlabels("/home/youssef/Desktop/Sordi_poc/Sordi_poc_10k","/home/youssef/Desktop/Sordi_poc/Synth_PoC100%[7k]")