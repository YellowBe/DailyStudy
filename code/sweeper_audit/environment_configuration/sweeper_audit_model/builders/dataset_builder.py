import os
import pickle
from torch.utils import data
from dataset.sweeper import SweeperDataSet, SweeperValDataSet, SweeperTrainInform, SweeperTestDataSet
import cv2
import numpy as np
import shutil

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.png'):
                fullname = os.path.join(root, f)
                yield fullname


def dataset_update(data_dir, train_data_list, val_data_list):
    base_dataset = 'sweeper'
    train_base_path = 'train'
    train_image_base = './dataset/'+base_dataset+'/'+train_base_path
    train_write_file=open(train_data_list,'w')
    val_write_file=open(val_data_list,'w')
    split_count = 0
    for i in findAllFile(train_image_base):
        # print(i.split('/')[-1].split('i')[0])
        if split_count % 6 != 0:
            img_p = './train/' + i.split('/')[-1].split('i')[0] + 'img.png'
            ann_p = './trainannot/' + i.split('/')[-1].split('i')[0] + 'label.png'
            train_write_file.write(img_p+' '+ann_p+'\n')
        else:
            img_p = './train/' + i.split('/')[-1].split('i')[0] + 'img.png'
            ann_p = './trainannot/' + i.split('/')[-1].split('i')[0] + 'label.png'
            val_write_file.write(img_p+' '+ann_p+'\n')
        split_count += 1
    train_write_file.close()
    val_write_file.close()
    print('read name is done')

    train_label_base = './dataset/'+base_dataset+'/'+train_base_path+'_labelme'
    for i in findAllFile(train_label_base):
        image = cv2.imread(i)
        # print(i)
        for row in image:
            for element in row:
                if element[0]==0 and element[1]==128 and element[2]==0:
                    element[0],element[1],element[2]=1,1,1
                elif element[0]==0 and element[1]==0 and element[2]==128:
                    element[0],element[1],element[2]=2,2,2
                elif element[0]==0 and element[1]==128 and element[2]==128:
                    element[0],element[1],element[2]=3,3,3
        # dim = (480,360)
        # image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite('./dataset/'+base_dataset+'/'+train_base_path+'annot/'+i.split('/')[-1],image)
    print('resize label is done')


def build_dataset_train(dataset, build_new_dataset, input_size, batch_size, train_type, random_scale, random_mirror, num_workers):
    data_dir = os.path.join('./dataset/', dataset)
    dataset_list = dataset + '_train_list.txt'
    train_data_list = os.path.join(data_dir, dataset + '_' + train_type + '_list.txt')
    val_data_list = os.path.join(data_dir, dataset + '_val' + '_list.txt')
    # inform_data_file = os.path.join('/home/guohao/code/Efficient-Segmentation-Networks/dataset/inform/', dataset + '_inform.pkl')
    if build_new_dataset:
        print('dataset update')
        dataset_update(data_dir, train_data_list, val_data_list)
    inform_data_file = './dataset/sweeper/new_inform.pkl'
    # inform_data_file collect the information of mean, std and weigth_class
    if build_new_dataset:
        if dataset == 'sweeper':
            dataCollect = SweeperTrainInform(data_dir, 4, train_set_file=dataset_list,
                                            inform_data_file=inform_data_file)
        else:
            raise NotImplementedError(
                "This repository now supports sweeper, %s is not included" % dataset)

        datas = dataCollect.collectDataAndSave()
        if datas is None:
            print("error while pickling data. Please check.")
            exit(-1)
        print('inform file is done')
    else:
        print("find file: ", str(inform_data_file))
        datas = pickle.load(open(inform_data_file, "rb"))

    if dataset == "sweeper":
        trainLoader = data.DataLoader(
            SweeperDataSet(data_dir, train_data_list, crop_size=input_size, scale=random_scale,
                          mirror=random_mirror, mean=datas['mean'], ignore_label=0),
            batch_size=batch_size, shuffle=True, num_workers=num_workers,
            pin_memory=True, drop_last=True)

        valLoader = data.DataLoader(
            SweeperValDataSet(data_dir, val_data_list, f_scale=1, mean=datas['mean']),
            batch_size=1, shuffle=True, num_workers=num_workers, pin_memory=True)

        return datas, trainLoader, valLoader


def build_dataset_test(dataset, num_workers, none_gt=False):
    data_dir = os.path.join('./dataset/', dataset)
    dataset_list = dataset + '_train_list.txt'
    test_data_list = os.path.join(data_dir, dataset + '_test' + '_list.txt')
    # inform_data_file = os.path.join('/home/guohao/code/Efficient-Segmentation-Networks/dataset/inform/', dataset + '_inform.pkl')
    inform_data_file = './dataset/sweeper/new_inform.pkl'
    # inform_data_file collect the information of mean, std and weigth_class
    print("find file: ", str(inform_data_file))
    datas = pickle.load(open(inform_data_file, "rb"))

    if dataset == "Sweeper":

        testLoader = data.DataLoader(
            SweeperValDataSet(data_dir, test_data_list, mean=datas['mean']),
            batch_size=1, shuffle=False, num_workers=num_workers, pin_memory=True)

        return datas, testLoader
