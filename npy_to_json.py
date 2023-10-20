import os

import numpy as np
import json
import shutil

def npy_to_json(files_directory):

    directories=os.listdir(files_directory)
    np_load_old = np.load
    # modify the default parameters of np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)

    for dir in directories:
        #current_dir=files_directory+ '/'+  dir +'/Viewport/rgb'
        #new_dir_name='images'
        #new_dir = os.path.join(os.path.dirname(current_dir), new_dir_name)
        #os.rename(current_dir, new_dir)
        output = files_directory +'/'+ dir +'/labels/json/'
        create_folder(output)
        npys=os.listdir(files_directory+ '/'+  dir +'/bbox_2d_tight/')

        for npy in npys :
            npy_array = np.load(files_directory +'/'+ dir +'/bbox_2d_tight/' + npy)
            jsonfile = npy.split('.')[-2] + ".json"
            #print(npy_array.tolist())

            labels=[]

            for label in npy_array.tolist():
                labels_dict = {}
                labels_dict['Id']=label[0]
                labels_dict['ObjectClassName'] = label[2]
                labels_dict['Left'] = label[6]
                labels_dict['Top'] = label[7]
                labels_dict['Right'] = label[8]
                labels_dict['Bottom'] = label[9]
                #print(labels_dict)
                labels.append(labels_dict)
                #print(labels)

            # Save the dictionary to a JSON file
            with open(files_directory +'/'+ dir +'/labels/json/'+ jsonfile, 'w') as json_file:
                json.dump(labels, json_file)

        #shutil.rmtree(files_directory +'/'+ dir +'/Viewport/bbox_2d_tight/')

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

npy_to_json('/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath/Sordi4/output3/')