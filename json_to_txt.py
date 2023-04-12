import os
import json
import shutil

def txt_writer(files_directory):
    #path = files_directory + '/datasets/'
    json_path = files_directory + "/labels/json/"
    if 'json' in os.listdir(files_directory + '/labels/'):
        output = files_directory + "/labels/yolo/"
        create_folder(output)
        # Get the labels
        labels_list = os.listdir(json_path)
        print(labels_list)
        for labels in labels_list:
            out_list = []
            with open(files_directory + "/labels/json/" + labels,'r') as f:
                json_file = json.load(f)
            for label in json_file:
                print(get_vector(label))
                out_list.append(get_vector(label))
            file = open(output + labels.split('.')[0] + '.txt', 'w')
            for item in out_list:
                file.write(item + "\n")
            file.close()

        shutil.rmtree(json_path)

def get_vector(json_data):

    label_list = ["klt_box","stillage","fire_extinguisher","pallet","jack","dolly"]

    width = abs(json_data['Left'] - json_data['Right'])
    height = abs(json_data['Top'] - json_data['Bottom'])

    x_center = (width / 2 + json_data['Left']) / 1280
    y_center = (height / 2 + json_data['Top']) / 720

    normalized_width=width / 1280
    normalized_height=height / 720

    return f"{label_list.index(json_data['ObjectClassName'])} {x_center} {y_center} {normalized_width} {normalized_height} "

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

txt_writer('/home/youssef/Desktop/Training_Dataset(15k)/DR1_Dataset')
