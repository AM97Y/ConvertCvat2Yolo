
#https://blog.paperspace.com/train-yolov7-custom-data/
import os
import xml.etree.ElementTree as ET
path = 'test_convert/video'
dataset_path = 'test_convert/video/drone_dataset'
for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            images_path = f"{dataset_path}/images/{file.split('.')[0]}"

            if not os.path.exists(images_path):
                os.makedirs(images_path)

            os.system(f"ffmpeg -i {path}/{file} {images_path}/%d.jpg")

            #SERVER_PATH = "test_convert"
            # SERVER_PATH = "data/DGX-1_uniyar/home/d.grushevskaya1/projects/dron_maks"

            ANNOTAIONS_DIR = f"{path}/{file.split('.')[0]}/annotations.xml"
            tree = ET.parse(ANNOTAIONS_DIR)
            root = tree.getroot()
            width, height = 0, 0
            for member in root.iter('original_size'):
                width = float(member.find("width").text)
                height = float(member.find("height").text)

            file_name = ''
            for member in root.iter('meta'):
                file_name = member.find("source").text
                if file != file_name:
                    print(f"Error ann for {file}")
                    print(file.split('.')[0], file_name)


            for member in root.iter('track'):
                label = 0#member.get('label')
                for box in member.findall('box'):
                  frame = float(box.get('frame'))
                  xtl = float(box.get('xtl'))
                  ytl = float(box.get('ytl'))
                  xbr = float(box.get('xbr'))
                  ybr = float(box.get('ybr'))
                  new_xc = (xtl + (xbr - xtl) / 2) / width
                  new_yc = (ytl + (ybr - ytl) / 2) / height
                  new_w = (xbr - xtl) / width
                  new_h = (ybr - ytl) / height

                  labels_path = f'{dataset_path}/labels/{file.split(".")[0]}'
                  if not os.path.exists(labels_path):
                    os.makedirs(labels_path)
                  with open(f"{labels_path}/{int(frame)}.txt", 'w') as f:
                      f.write(f'{label} {new_xc} {new_yc} {new_w} {new_h}\n')




