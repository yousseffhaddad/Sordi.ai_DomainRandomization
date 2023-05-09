import os
import json
import matplotlib.pyplot as plt
import cv2
import random
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

    #asset_percentage_dic = {"stillage": 0, "dolly": 0, "klt_box": 0, "fire_extinguisher": 0, "jack": 0, "pallet": 0,}
    asset_percentage_dic={ "stillage": 0,"dolly": 0 }
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

    #data = json.load(open(source_directory + '/objectclasses.json'))
    #assets_needed = ["klt_box", "stillage", "fire_extinguisher", "pallet", "jack", "dolly"]
    assets_needed = ["stillage","dolly"]
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
            if ct%100==0 :
                asset=check_percentage(source_directory,selected_items,assets_needed)
                print(asset)
            for j in range (len(obj)):
                if obj[j]['ObjectClassName']==asset :
                    selected_items.append(item)
                    random_items.remove(item)
                    ct = ct + 1
                    print(ct)
                    break
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
            cv2.imwrite(destination_directory + '/images/' + str(i) + '.png', image)
            obj = json.load(open(source_directory + '/labels/json/' + label))
            open(destination_directory + '/labels/json/'+ str(i) +'.json', "w").write(
                json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
            )
            i=i+1

    else :
        print ("your nb of images that you provided exceed the capacity ")

def transfer_regen(source_directory,destination_directory):

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
        i=i+1



'''def transfer_data (source_directory,destination_directory,nb_of_images):

    data = json.load(open(source_directory + '/objectclasses.json'))
    assets_needed = ["klt_box", "stillage", "fire_extinguisher", "pallet", "jack", "dolly"]
    if nb_of_images <= len(os.listdir(source_directory + '/labels/json/')) :

        open(destination_directory + '/objectclasses.json', "w").write(
            json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
        )

        labels = os.listdir(source_directory + '/labels/json/')
        i=len(os.listdir(destination_directory + '/labels/json/')) +1

        print("I IS :",i)

        random_items = random.sample(labels,len(os.listdir(source_directory + '/labels/json/')))
        selected_items=[]

        for item in labels :
            obj = json.load(open(source_directory + '/labels/json/' + item))
            for j in range (len(obj)):
                if obj[j]['ObjectClassName']=='fire_extinguisher' or  obj[j]['ObjectClassName']=='stillage' :
                    selected_items.append(item)
                    random_items.remove(item)
                    break
        print(len(selected_items))
        #print(random_items)
        if len(selected_items)>nb_of_images:
            random_items=random.sample(selected_items,nb_of_images)
        else:
            random_items=random.sample(random_items,nb_of_images-len(selected_items)) +selected_items
        print(len(random_items))
        for label in random_items :

            label_corresponding_image = label.split('.')[-2] + ".jpg"
            image = cv2.imread(source_directory + '/images/' + label_corresponding_image)
            cv2.imwrite(destination_directory + '/images/' + str(i) + '.jpg', image)
            obj = json.load(open(source_directory + '/labels/json/' + label))
            open(destination_directory + '/labels/json/'+ str(i) +'.json', "w").write(
                json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
            )
            #print(i)
            i=i+1

    else :
        print ("your nb of images that you provided exceed the capacity ")'''

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

def drawBox(boxes,image):

    cv2.rectangle(image, (boxes[0], boxes[1]), (boxes[2], boxes[3]), (255, 0, 0),2)
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

#Calling functions

'''image = cv2.imread('/home/youssef/Desktop/Sordi.ai_Dataset/STR_export_230419074900/images/0015000695.png')
image_label = json.load(open('/home/youssef/Desktop/Sordi.ai_Dataset/STR_export_230419074900/labels/json/0015000695.json'))
origLeft = int(image_label[0]["Left"])
origTop = int(image_label[0]["Top"])
origRight = int(image_label[0]["Right"])
origBottom = int(image_label[0]["Bottom"])
#print(origBottom,origTop,origRight,origLeft)

drawBox([origLeft, origTop, origRight, origBottom],image)'''




#assets_needed=["klt_box","stillage","fire_extinguisher","pallet","jack","dolly"]
assets_needed=["stillage","dolly"]
#print(check_percentage('/home/youssef/Desktop/Sordi.ai_Dataset/Sordi_POC',assets_needed))

#pp.remove_duplicates_using_hash('/home/youssef/Desktop/Training_Dataset(15k)/Reg_rand+fllwpath70%')
#pp.change_subassets_names('/home/youssef/Desktop/Sordi.ai_Dataset/Sordi-Datasets/Sordi4/output3/resized6/Viewport')
#pp.delete_uneeded_assets('/home/youssef/Desktop/Sordi.ai_Dataset/Sordi-Datasets/Sordi4/output3/resized6/Viewport')
#pp.delete_empty_files('/home/youssef/Desktop/Sordi.ai_Dataset/Sordi-Datasets/Sordi4/output3/resized6/Viewport')
#pp.change_subassets_names('/home/youssef/Desktop/Sordi.ai_Dataset/youssef/W_Eval_200')
#pp.adjust_object_class_name('/home/youssef/Desktop/Sordi.ai_Dataset/SORDI-Real_export_230421064237')

#pp.renaming_Object_Class_Id('/home/youssef/Desktop/Evaluation_Dataset/Eval6new1')

#pp.add_object_class_id('/home/youssef/Desktop/Training_Dataset(15k)/Reg_fllwpath100%')


#pp.delete_json('/home/youssef/Desktop/Training_Dataset/No-DR')
#pp.delete_images('/home/youssef/Desktop/Sordi.ai_Dataset/Spartunburg')
#da.augment_data('/home/youssef/Desktop/Training_Dataset30k/DR2(30k)','/home/youssef/Desktop/Training_Dataset30k/DR2_Aug(30k)')
#print(len(os.listdir('/home/youssef/Desktop/Training_Dataset(15k)/Reg_fllwpath100%/images')))
#print(len(os.listdir('/home/youssef/Desktop/Training_Dataset(15k)/Reg_fllwpath100%/labels/json')))
#transfer_data('/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath_Synthetic/Sordi4/output3/resized6/Viewport','/home/youssef/Desktop/Training_Dataset(15k)/Reg_fllwpath100%',420)
#check_percentage_histogram('/home/youssef/Desktop/Training_Dataset(15k)/Reg_rand+fllwpath30%',assets_needed)

#delete('/home/youssef/Desktop/Training_Dataset(15k)/FllwPath_regen100%',1939)
#/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath_Synthetic/Sordi2/output1/resized/Viewport jpg
#/home/youssef/Desktop/Sordi.ai_Dataset/regensburg_plant_720p  jpg
#/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath_Real png


#transfer_regen('/home/youssef/Desktop/Sordi.ai_Dataset/STR_export_230419074900','/home/youssef/Desktop/Evaluation_Dataset/Exp3_Eval')