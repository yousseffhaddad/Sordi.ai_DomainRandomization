import numpy as np
import cv2
import os
import json


def dhash(image, hashSize=8):
	# convert the image to grayscale and resize the grayscale image,
	# adding a single column (width) so we can compute the horizontal
	# gradient
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	resized = cv2.resize(gray, (hashSize + 1, hashSize))
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash and return it
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def remove_duplicates_using_hash (files_directory) :
  print("[INFO] computing image hashes...")
  imagePaths = os.listdir(files_directory + '/images/')
  hashes = {}

  # loop over our image paths
  for imagePath in imagePaths:
      # load the input image and compute the hash
      image = cv2.imread(files_directory + '/images/' + imagePath)
      h = dhash(image)
      # grab all image paths with that hash, add the current image
      # path to it, and store the list back in the hashes dictionary
      p = hashes.get(h, [])
      p.append(imagePath)
      hashes[h] = p

  dup_counter = {}
  total_deleted_images = 0
  # loop over the image hashes
  for (h, hashed_paths) in hashes.items():
    count=0
    # check to see if there is more than one image with the same hash
    if len(hashed_paths) > 1:
      for p in hashed_paths[1:]:
        os.remove(files_directory + '/images/' +p)
        print(p, " removed")
        image_corresponding_label = p.split('.')[-2] + ".json"
        for image_label in os.listdir(files_directory + '/labels/json/'):
          if (image_label == image_corresponding_label):
            os.remove(files_directory + '/labels/json/'+ image_label)
            print(image_label, " removed")
            break
        count += 1
      dup_counter[hashed_paths[0]] = str(count+1)
      total_deleted_images += count
  return dup_counter, total_deleted_images


def delete_uneeded_assets (files_directory : str):
  # Load the JSON module and use it to load your JSON file.
  # I'm assuming that the JSON file contains a list of objects.
  print("deleting uneeded assets ...")
  #assets_needed = {"klt_box": 1015, "stillage": 1004, "fire_extinguisher": 5010, "pallet": 1100, "jack": 1120,"dolly": 1110}
  assets_needed=["stillage","dolly"]
  labels = os.listdir(files_directory + '/labels/json/')
  for label in labels :
      obj  = json.load(open(files_directory + '/labels/json/' + label))
      new_json = {}
      j=0
      # Iterate through the objects in the JSON and pop (remove)
      # the obj once we find it.
      for i in range(len(obj)):
        if obj[i]["ObjectClassName"] in assets_needed:
              new_json[j]= obj[i]
              j += 1

      final_json_version = [val for key, val in new_json.items()]

      # Output the updated file with pretty JSON
      open(files_directory + '/labels/json/' + label, "w").write(
          json.dumps(final_json_version, sort_keys=False, indent=4, separators=(',', ': '))

      )



def delete_empty_files (files_directory : str):
  print("deleting empty files")
  for filename in os.listdir(files_directory + '/labels/json/'):
    data = json.load(open(files_directory + '/labels/json/' + filename))
    if not data :
      label_corresponding_image = filename.split('.')[-2] + ".png"
      os.remove(files_directory + '/labels/json/' + filename)
      if os.path.exists(files_directory + '/images/' + label_corresponding_image):
          os.remove(files_directory + '/images/' + label_corresponding_image)
      print(f"File {filename} has been deleted")



def delete_images (files_directory : str):
  print("deleting images")
  for filename in os.listdir(files_directory + '/images/'):

      image_corresponding_label = filename.split('.')[-2] + ".json"
      if not os.path.exists(files_directory + '/labels/json/' + image_corresponding_label):
                os.remove(files_directory + '/images/' + filename)
      print(f"File {filename} has been deleted")



def delete_json (files_directory : str):
  print("deleting images")
  for filename in os.listdir(files_directory + '/labels/json/'):

      label_corresponding_image = filename.split('.')[-2] + ".jpg"
      if not os.path.exists(files_directory + '/images/' + label_corresponding_image):
                os.remove(files_directory + '/labels/json/' + filename)
                print(f"File {filename} has been deleted")



def change_subassets_names (files_directory : str):
  print("changing subassets names...")
  sub_assets={"klt_box":["klt_box_empty","klt_box_full","l_klt_4147","l_klt_8210","l_klt_3147","l_klt_6147","l_klt_6410","box_klt"],
                "stillage":["stillage_full","stillage_empty","stillage_close","stillage_open","stillage_front_310_6969","Meshcontainer"]
           }

  for filename in os.listdir(files_directory + '/labels/json/'):
    data = json.load(open(files_directory + '/labels/json/' + filename))
    for i in range(len(data)):
        if data[i]["ObjectClassName"] in sub_assets['klt_box']:
            data[i]["ObjectClassName"]='klt_box'

        if data[i]["ObjectClassName"] =="Dolly":
            data[i]["ObjectClassName"]='dolly'

        elif data[i]["ObjectClassName"] in sub_assets['stillage']:
            data[i]["ObjectClassName"] = 'stillage'

    open(files_directory + '/labels/json/' + filename, "w").write(
        json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
    )

  print("done")



def adjust_object_class_name (files_directory : str):

    print("adjusting object classes names")
    data = json.load(open(files_directory + '/objectclasses.json'))
    #assets_needed = {"klt_box": 1015, "stillage": 1004, "fire_extinguisher" : 5010, "pallet": 1100, "jack": 1120, "dolly": 1110}
    assets_needed = { "stillage": 1004, "dolly": 1110, "str":2050}
    new_json={}
    i=0
    for key , val  in assets_needed.items():
        data[i]['Name']=key
        data[i]['Id']=val
        new_json[i] = data[i]
        i=i+1

    final_json_version = [val for key, val in new_json.items()]
    # Output the updated file with pretty JSON
    open(files_directory + '/objectclasses.json', "w").write(
        json.dumps(final_json_version, sort_keys=False, indent=4, separators=(',', ': '))
    )

def renaming_Object_Class_Id(files_directory : str):

    for filename in os.listdir(files_directory + '/labels/json/'):
        data = json.load(open(files_directory + '/labels/json/' + filename))
        for i in range(len(data)):
            if data[i]["ObjectClassName"] == 'klt_box' :
                data[i]["ObjectClassId"] = 1015

            elif data[i]["ObjectClassName"] == "stillage" :
                data[i]["ObjectClassId"] = 1004

        open(files_directory + '/labels/json/' + filename, "w").write(
            json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
        )

    print("done")

def add_object_class_id (files_directory : str):

    assets_needed = {"klt_box": 0, "stillage": 1004, "fire_extinguisher": 5010, "pallet": 1100, "jack": 1120,"dolly": 1110}
    assets_needed = {"stillage": 1004, "dolly": 1110}
    for filename in os.listdir(files_directory + '/labels/json/'):
        data = json.load(open(files_directory + '/labels/json/' + filename))
        for i in range(len(data)):

            data[i]["ObjectClassId"] = assets_needed[data[i]["ObjectClassName"]]

        open(files_directory + '/labels/json/' + filename, "w").write(
            json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
        )

    print("done")
