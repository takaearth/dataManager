import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            filename = root.find('filename').text
            width = int(root.find('size')[0].text)
            height = int(root.find('size')[1].text)
            obj_class = member[0].text

            # Check if 'bndbox' exists (which should be member[4] based on your script)
            bndbox = member.find('bndbox')
            if bndbox is not None:
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
            else:
                # If 'bndbox' is missing, skip this object or handle appropriately
                print(f"Missing 'bndbox' in file: {xml_file}")
                continue

            value = (filename, width, height, obj_class, xmin, ymin, xmax, ymax)
            xml_list.append(value)
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    for folder in ['train', 'validation']:
        image_path = os.path.join(os.getcwd(), ('images/' + folder))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(('images/' + folder + '_labels.csv'), index=None)
        print(f'Successfully converted XML to CSV for {folder} folder.')

main()
