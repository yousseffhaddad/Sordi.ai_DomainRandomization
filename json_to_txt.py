import os
import json
import shutil
def txt_writer(files_directory):

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

'''image_path = '/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Training_Dataset_30k/DR2(30k)/images/1.jpg'
image = cv2.imread(image_path)

# Load the corresponding YOLO label file
label_path = '/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Training_Dataset_30k/DR2(30k)/labels/yolo/1.txt'
with open(label_path, 'r') as f:
    lines = f.readlines()

# Loop through each line in the label file
for line in lines:
    parts = line.strip().split()
    class_id = int(parts[0])
    x_center = float(parts[1])
    y_center = float(parts[2])
    width = float(parts[3])
    height = float(parts[4])

    # Convert YOLO format to image coordinates
    image_height, image_width, _ = image.shape
    x = int((x_center - width / 2) * image_width)
    y = int((y_center - height / 2) * image_height)
    w = int(width * image_width)
    h = int(height * image_height)

    # Draw the bounding box
    color = (0, 255, 0)  # Green color for the box (BGR format)
    thickness = 2       # Thickness of the box's lines
    cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)

# Display the result
plt.figure(figsize=(10, 10))
plt.axis('off')
plt.imshow(image)
plt.show()'''
