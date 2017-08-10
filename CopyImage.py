import numpy as np
import os
from os import listdir
import sys
from shutil import copyfile

'''
get array of files' position in each part:

input:
    partsNum: number of parts
    filesNum: number of files
return:
    array of files' position(in list files) in each part
'''

def getSubFilesPosition(partsNum, filesNum):
    filesPosition = np.arange(filesNum)
    np.random.shuffle(filesPosition)
    filesNumInPart = filesNum//partsNum
    y = filesNum - filesNumInPart*partsNum
    x = partsNum - y
    filesNumInParts = np.concatenate((filesNumInPart*np.ones((x,), dtype=np.int), (filesNumInPart+1)*np.ones((y,), dtype=np.int)), axis = 0)
    np.random.shuffle(filesNumInParts)
    index = 0
    filesPositionInPart = list()
    for num in filesNumInParts:
        temp = filesPosition[index: index + num]
        index += num
        filesPositionInPart.append(temp)
    return filesPositionInPart


'''
copy listFile from rootFolder to partsNum parts to destination
'''

def separateFilesInSubFolder(rootFolder, folderName, listFile, partsNumber = 5, destination = '.'):
    filesNumber = len(listFile)
    filesPositionInParts = getSubFilesPosition(partsNum = partsNumber, filesNum = filesNumber)
    for i in range(len(filesPositionInParts)):
        for position in filesPositionInParts[i]:
            fileName = listFile[position]
            destPath = os.path.join(destination + 'part_' + str(i),folderName)
            if not os.path.exists(destPath):
                os.makedirs(destPath)
            copyfile(os.path.join(rootFolder, fileName), os.path.join(destPath, fileName))

'''
List all (only) files in a directory
'''

def files(path):
    listFile = list()
    for file1 in os.listdir(path):
        if os.path.isfile(os.path.join(path, file1)):
            listFile.append(file1)
    return listFile


'''
copy listFile from rootFolder to partsNum parts to destination
'''

def separateFilesInMasterFolder(rootFolder, partsNumber = 5, destination = '.'):
    subFolders = listdir(rootFolder)
    for subFolder in subFolders:
        subRealPath = os.path.join(rootFolder, subFolder)
        print subRealPath
        if os.path.isdir(subRealPath):
            listFile = files(subRealPath)
            print 'list file', listFile
#             listFile = listdir(subRealPath)
            separateFilesInSubFolder(rootFolder = subRealPath, folderName = subFolder, listFile = listFile, partsNumber = partsNumber, destination = destination)


if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) !=4:
        print 'lack of parameters including rootFolder, partsNumber and destination'
        print 'python CopyImage.py rootFolder partsNumber destination'
    else:
        # try:
        rootFolder = sys.argv[1]
        partsNumber = int(sys.argv[2])
        destination = sys.argv[3]
        separateFilesInMasterFolder(rootFolder, partsNumber = partsNumber, destination = destination)
        # except:
        #     print 'wrong parameter'
        #     print 'python CopyImage.py rootFolder partsNumber destination'