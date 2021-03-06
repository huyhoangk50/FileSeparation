import sys
import numpy as np
import pandas as pd
from PIL import Image
import csv
import os


def assignLabel(rootPath, dictPath):
    FIELD_NAMES = ['id', 'label']
    dirs = list()
    imageLabels = list()
    subDirs = list()
    subDirLabels = list()
    try:
        dictionary = pd.read_csv(dictPath)
        ids = dictionary["id"]
        ids = ids.as_matrix()
        csv_labels = dictionary["label"]
        csv_labels=csv_labels.as_matrix()
        nIds = ids.shape[0]

    except IOError, EmptyDataError:
        dictionary = None
        label_id = 0
    except pd.io.common.EmptyDataError:
        dictionary = None
        label_id = 0
    for sub_dir_flower in os.listdir(rootPath):
            folderPath = os.path.join(rootPath, sub_dir_flower)
            if dictionary is not None:
                try:
                    # print sub_dir_flower
                    # print ids
                    temp = np.where(ids == int(sub_dir_flower))[0]
                except ValueError:
                    temp = np.where(ids == str(sub_dir_flower))[0]
                    # print 'error'
                    # print temp
                if temp.shape[0] != 0:
                    label_id = csv_labels[temp[0]]
                else: 
                    label_id = nIds
                    print ids, sub_dir_flower
                    ids = np.append(ids, sub_dir_flower)
                    csv_labels = np.append(csv_labels, label_id)
                    nIds = nIds + 1 
            # subDirs.append(sub_dir_flower)
            # subDirLabels.append(label_id)
            for img in os.listdir(folderPath):
                try:
                    imagePath = os.path.join(folderPath, img)
                    pic = Image.open(imagePath)
                except IOError:
                    continue
                if (pic.format != 'JPEG'):
                    rgb_pic = pic.convert('RGB')
                    rgb_pic.save(imagePath)

                dirs.append(imagePath)
                imageLabels.append(label_id)
            if dictionary is None:
                if 'ids' not in locals():
                    ids = np.array(sub_dir_flower)
                    csv_labels = np.array(label_id)
                else:
                    ids = np.append(ids, sub_dir_flower)
                    csv_labels = np.append(csv_labels, label_id)
                label_id = label_id + 1
    dictRecords = np.asarray([ids, csv_labels]).T
    with open(dictPath, 'wb') as dictFile:
        writer = csv.writer(dictFile)
        writer.writerow(FIELD_NAMES)
        writer.writerows(dictRecords)
    return dirs, imageLabels

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'lack of parameters including dictPath, destPath rootPaths'
    else:
        dictPath = sys.argv[1]
        destPath = sys.argv[2]
        rootPaths = sys.argv[3:]

        # testFolders = sys.argv[2]
        file = open(destPath, 'a')
        for rootPath in rootPaths:
            dirs, imageLabels = assignLabel(rootPath, dictPath)
            for i in range(len(dirs)):
                file.write(dirs[i] + " " + str(imageLabels[i]) + "\n")
        file.close()