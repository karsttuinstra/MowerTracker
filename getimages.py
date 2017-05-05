import urllib
import cv2
import numpy as np
import os

def store_raw_images():
    #neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03417749'
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n12146654'
    neg_images_urls = urllib.urlopen(neg_images_link).read().decode()
    pic_num = 740

    if not os.path.exists('neg'):
        os.makedirs('neg')

    for i in neg_images_urls.split('\n'):
        try:
            print i
            urllib.urlretrieve(i, 'neg/' + str(pic_num) + '.jpg')
            img = cv2.imread('neg/' + str(pic_num) + '.jpg')
            resized_image = cv2.resize(img, (100,100))
            cv2.imwrite('neg/' + str(pic_num) + '.jpg', resized_image)
            pic_num += 1
        except Exception as e:
            print str(e)

#store_raw_images()

def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_images_path = str(file_type) + '/' + str(img)
                    ugly = cv2.imread('uglies/' + str(ugly))
                    question = cv2.imread(current_images_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly, question).any()):
                        print 'that is an ugly picture!'
                        print current_images_path
                        os.remove(current_images_path)
                except Exception as e:
                    print str(e)

#find_uglies()

def create_pos_n_neg():
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            if file_type == 'pos':
                line = file_type +'/'+img+' 1 0 0 50 50 \n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)
                
#create_pos_n_neg()