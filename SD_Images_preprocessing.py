import cv2
import os
import json
def save_frames(video_path, output_folder):
    create_folder(output_folder)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(round(fps / 3))  # Save 3 frames per second
    #for example if we have fps 30 so frame inter is 10 then we get one image each 10 frames within the laplacian threshold
    count = 0
    print(fps)
    print(frame_interval)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        frames.append(frame)
        if not ret:
            break

        if len(frames) % frame_interval == 0:
            for f in frames:
                # Apply Laplacian function to avoid blur
                gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
                laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()
                print(laplacian)
                if laplacian > 20:  # Adjust the threshold to your needs
                    output_path = f"{output_folder}/frame_{count}.jpg"
                    print(output_path)
                    cv2.imwrite(output_path, frame)
                    frames = []
                    break
            frames = []
        count += 1

    cap.release()

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def addingCap(files_directory):

    #labels = os.listdir(files_directory + '/labels/json/')
    images = os.listdir(files_directory)
    #assets=[]
    #output = files_directory + "/Cap/"
    #create_folder(output)
    for label in images :
        #obj = json.load(open(files_directory + '/labels/json/' + label))
        #for i in range(len(obj)):
            #assets.append(obj[i]["ObjectClassName"])
        #assets=list(set(assets))
        file = open(files_directory + label.split('.')[0] + '.txt', 'w')

        #file.write(",".join(assets))

        file.write("Klt_box")

        file.close()
        #assets=[]

def renameImages(files_directory):
    images = os.listdir(files_directory)
    i=1
    for img in images :
        if img.split('.')[-1] == 'jpg':
            os.rename(files_directory + img.split('.')[-2]+'.txt', files_directory + str(i) + '.txt')
            os.rename(files_directory + img,files_directory + str(i) + '.jpg')
            i=i+1

def delete_txt(files_directory):
    images = os.listdir(files_directory)

    for img in images :
        if img.split('.')[-1] == 'txt':
            os.remove(files_directory + img)


def resize_Images(files_directory):
    images = os.listdir(files_directory)
    new_size = (512, 512)
    for img in images :

        if img.split('.')[1] != 'txt':

            image = cv2.imread(files_directory +'/'+ img)
            # Set the desired new size


            # Resize the image
            resized_image = cv2.resize(image, new_size)

            # Save the resized image
            cv2.imwrite(files_directory + '/' +img, resized_image)

def transfer_data(source_directory, destination_directory):

        items = os.listdir(source_directory)
        i = int(len(os.listdir(destination_directory)))
        #i=int(len(os.listdir(destination_directory))/2 +1)
        #j = int(len(os.listdir(destination_directory))/2+ 1)

        print("I IS :", i)

        for item in items:
            if i==4089:
                break
            if item.split('.')[-1] == 'jpg':
                image = cv2.imread(source_directory + item)
                cv2.imwrite(destination_directory + str(i) + '.jpg', image)
                i = i + 1
            '''else:
                print("hello")
                with open(source_directory + item, "r") as file:
                    # Read the content of the file
                    content = file.read()
                file = open(destination_directory + str(j) + '.txt', 'w')

                file.write(content)
                j = j + 1'''


def delete_images_without_txt(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            image_file = os.path.join(folder_path, filename)
            txt_file = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")

            if not os.path.exists(txt_file):
                print(f"Deleting {filename} as there is no corresponding txt file.")
                os.remove(image_file)


def is_blurry(image_path, threshold=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return False  # Skip if the image couldn't be loaded

    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
    return laplacian_var < threshold


def remove_blurry_images(directory_path,destination_directory ,threshold=100):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(directory_path, filename)
            if is_blurry(image_path, threshold):
                os.remove(image_path)
                #copy images to other directory

                '''label_corresponding_image = filename.split('.')[-2] + ".json"
                image = cv2.imread(image_path)
                cv2.imwrite(destination_directory + '/images/' + filename, image)
                obj = json.load(open('/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/evaluation_Exp3_Munich/labels/json/' + label_corresponding_image))
                open(destination_directory + '/labels/json/' + label_corresponding_image, "w").write(
                    json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))
                )
                print(f"Removed blurry image: {filename}")'''


# Specify your directory containing images
image_directory = '/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/evaluation_Exp3_Munich(After_cleaning)/images/'
dest='/media/youssef/9e108ea8-f054-471a-8046-77291aab9175/home/youssef/Documents/Evaluation_Dataset/evaluation_Exp3_Munich/blurry_images'
# Set a threshold value for blurriness detection
blur_threshold = 200

#remove_blurry_images(image_directory,dest, blur_threshold)


#delete_images_without_txt("/home/youssef/Desktop/Real_Images/After_adjusting/Klt_box,pallet_new/")
#renameImages('/home/youssef/Desktop/Real_Images/After_adjusting/Klt_box,pallet_new/')
#print(len(os.listdir("/home/youssef/Desktop/Real_Images/After_adjusting/jack/")))
#transfer_data('/home/youssef/Desktop/Real_Images/R_KltBox/images/','/home/youssef/Desktop/Real_Images/Real_Images_9categories/Klt_box/images/')
#resize_Images('/home/youssef/Desktop/Real_Images/drive-download-20230801T142256Z-001/dolly,pallet')
#delete_txt('/home/youssef/Desktop/Real_Images/BlueJacks/')
#Usage example
#video_path = "/home/youssef/Downloads/drive-download-20230801T142256Z-002/FullSizeRender(22).mov"
#output_folder = "/home/youssef/Downloads/drive-download-20230801T142256Z-002/FullSizeRender(22)"
#addingCap('/home/youssef/Desktop/Real_Images/After_adjusting/Klt_box,pallet_new/')
#save_frames(video_path, output_folder)

