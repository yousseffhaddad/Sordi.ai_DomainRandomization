import json
import os
import sys

files_directory = sys.argv[1]
labels = os.listdir(files_directory + "/labels/json/")
assets = {"klt_box": 0, "stillage": 0, "fire_extinguisher": 0, "pallet": 0, "jack": 0, "dolly": 0}
for asset in assets :
    print(asset)
    for label in labels:
        obj = json.load(open(files_directory + 'labels/json/' + label))
        for o in obj:
            if o["ObjectClassName"]==asset:
                assets[asset] += 1
                break
print(assets)