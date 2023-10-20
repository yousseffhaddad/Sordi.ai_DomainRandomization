import os
import json
import pandas as pd
import sys

def getAssetsName(file):
    obj = json.load(open(file))
    new_json = {}
    for i in range(len(obj)):
        key = obj[i].get('Name', None)
        if key is not None:
            new_json[key] = 0
        #new_json[i]['key']=obj[i]["Name"]

    open('datasets/config.json', "w").write(
        json.dumps(new_json, sort_keys=False, indent=4, separators=(',', ': '))

    )

#getAssetsName('datasets/config.json')

def countOcc(files_directory):
    labels = os.listdir(files_directory + '/labels/json/')
    conf = json.load(open('datasets/config.json'))
    for label in labels:
        obj = json.load(open(files_directory + '/labels/json/' + label))
        for i in range(len(obj)):
            if obj[i]["ObjectClassName"] in list(conf):
                conf[obj[i]["ObjectClassName"]]+=1

    open('datasets/config.json', "w").write(
        json.dumps(conf, sort_keys=False, indent=4, separators=(',', ': '))

    )

#countOcc('/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath/Sordi4/output3/6')

mainAssets={'logistic':['containers','stillage','stillage_front_310_6969','stillage_full','stillage_empty','stillage_close','stillage_open','klt_box','l_klt_4147','klt_box_empty','klt_box_full',
                        'l_klt_8210','l_klt_3147','l_klt_6147','f_klt_6410','gitter','gitter_black_stripped','gitter_close','gitter_open','cardboard_box','eps_box','bins','industrial_bin',
                        'wheelie_bin','garbage','storage','closed','locker','cabinet','rack','rack_1','rack_2','rack_3','rack_4','carrier_holder_lifter','pallet','lid','scissor_lift','barrier_setup',
                        'railing','metal_railing','guard_railing','safety','safety_gate','safety_cone','spring_post','robots','3d_printer','robotarm'],

            'transportation':['short_distance_transporter','dolly','trolley','jack','electrical_jack','tugger_cart','long_distance_transporter','str','carter','tugger_train','forklift',
                              'general','bicycle','scooter','tricycle','car'],

            'tools':['mechanical','axe','hacksaw','toolsaw','toothsaw','hammer','ladder','leveler','pliers','wrench','screwdriver','tapemeasure','cutter','bolt','nut','electric',
                     'chainsaw','power_drill','powerstrip','safety','safety_glove','safety_googles','first_aid_box','first_aid','fire_extinguisher'],

            'signage':['solid','exit_sign','stop_sign','first_aid_sign','fire_extinguisher_sign','wc_sign','wet_floor_sign','parking_sign','marking','stop_sign_marking','cross_stripes_marking',
                     'walking_marking','forklift_marking','logo','sordi_logo','bmw_group_logo','bmw_logo','minicooper_logo','rollsroyce_logo','bmw_qut_logo','microsoft_logo','nvidia_logo','idealworks_logo','inmind_logo','robotron_logo'],

            'office':['electronic_it','monitor','mouse','keyboard','laptop','headset','pc','kitchen','spoon','knife','fork','plate','mug','can','vending_machine','furniture',
                      'trash_can','chair','wall_clock','coat_hanger','mug','desk_table','table','plant','fan','stationery','white_board','marker_pen','puzzle_cube','hole_punch','pencil',
                      'stapler','eraser','sticky_notes','scissors','plastic_bottle']}


def CountHead_Asset(file,assets):
    obj = json.load(open(file))
    asset=''
    list_of_assets=[]
    for i in range(len(obj)):
        mainAssets = {'logistic': 0, 'transportation': 0, 'tools': 0, 'signage': 0, 'office': 0}
        for key, value in obj.items():
            for key1, value1 in assets.items():
                if key in value1 :
                    asset=key1
                    break
            mainAssets[asset]+=1
        print(i,"dataset : ","\n",mainAssets)
        #mainAssets['dataset']=obj[i]["dataset_name"]
        list_of_assets.append(mainAssets)

    open('datasets/config.json', "w").write(
        json.dumps(list_of_assets, sort_keys=False, indent=4, separators=(',', ': '))

    )


def convert_json_to_excel(json_file, excel_file):
    with open(json_file) as file:
        data = pd.read_json(file)

    data.to_excel(excel_file, index=False)

def Count_distinct_asset(files_directory):
    labels=os.listdir(files_directory)
    assets=[]
    for label in labels :
        obj = json.load(open(files_directory+label))
        for i in range(len(obj)):
            assets.append(obj[i]["ObjectClassName"])
    assets=list(set(assets))
    print(assets)
    print(len(assets))

def get_all_assets(file):
    folders=os.listdir(file)
    assets=[]
    for f in folders :
        for f1 in os.listdir(file+'/'+f):
            labels=os.listdir(file+'/'+f +'/'+f1+'/labels/json/')
            for label in labels :
                obj = json.load(open(file+'/'+f+'/'+f1+'/labels/json/'+label))
                for o in obj :
                 assets.append(o['ObjectClassName'])

    assets = list(set(assets))
    new_json = {}
    for s in assets :
        new_json[s] = 0

    open('datasets/config2.json', "w").write(
        json.dumps(new_json, sort_keys=False, indent=4, separators=(',', ': '))

    )

def find_correspending_labels(source_directory,destination_directory):
    source=os.listdir(source_directory)
    dest=os.listdir(destination_directory+"images/")
    for f in dest:
        if f.split('.')[-1]=='jpg':
            print(f)
            label_corresponding_image = f.split('.')[-2] + ".json"
            obj = json.load(open(source_directory+'labels/json/'+label_corresponding_image))
            open(destination_directory+'labels/json/'+label_corresponding_image, "w").write(
                json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))

            )

def Count_Object_Class (files_directory):
    files_directory = sys.argv[1]
    labels = os.listdir(files_directory+"/labels/json/")
    assets={"klt_box":0, "stillage":0, "fire_extinguisher":0, "pallet":0, "jack":0, "dolly":0}
    for label in labels :
        obj = json.load(open(files_directory + 'labels/json/' + label))
        for o in obj :
            if o["ObjectClassName"] in assets.keys():
                assets[o["ObjectClassName"]]+=1
    print(assets)


#find_correspending_labels('/home/youssef/Desktop/Eval_Dataset_GenAI/SORDI-Real_export_230421064237/','/home/youssef/Desktop/Eval_Dataset_GenAI/Eval/')
#get_all_assets('/home/youssef/Desktop/Sordi.ai_Dataset/FllwPath/Sordi4')
Count_distinct_asset('/home/youssef/Desktop/Sordi_poc/Sordi_poc/labels/json/')
#CountHead_Asset('datasets/config.json',mainAssets)
#convert_json_to_excel('datasets/config.json','output.xlsx')



