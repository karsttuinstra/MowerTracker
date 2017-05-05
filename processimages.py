import os
import glob
import csv
import cv2

#folder = 'files/20170504-140838BOOSTER150/'
#file = folder + 'neg20170504-140838.lst'
folder = 'files/20170504-133714MIL/'
file = folder + '20170504-133714.lst'
cropfolder = folder + 'info'

def processImage(file=file, cropfolder=cropfolder):
    if not os.path.exists(cropfolder):
        os.makedirs(cropfolder)

    f = open(cropfolder + 'info.lst', 'w+')

    with open(file) as inputfile:
        for row in csv.reader(inputfile, delimiter=' '):
            rawimage = cv2.imread(row[0], 0)
            roi = rawimage[int(row[3]) : (int(row[3]) + int(row[5])), int(row[2]) : (int(row[2]) + int(row[4]))]
            croppedname = row[0].replace(folder,"")
            f.write(row[0] + ' 1 0 0 300 300\n')
            print croppedname
            cv2.imwrite(os.path.join(cropfolder, croppedname),roi)

processImage()