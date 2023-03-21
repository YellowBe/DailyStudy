import os
import cv2 as cv
import shutil


def change_name(index, path):
    fileList=os.listdir(path)
    n = index
    for i in range(len(fileList)):
        #设置旧文件名（就是路径+文件名）
        oldname=path+ os.sep + fileList[i]   # os.sep添加系统分隔符
        #设置新文件名
        newname=path + os.sep +'raw'+str(n).zfill(4)+'.jpg'
        os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
        print(oldname,'======>',newname)
        n+=1

def image_preprocess(path,output_path):
    fileList=os.listdir(path)
    for i in range(len(fileList)):
        imagename=path+ os.sep + fileList[i]
        outputname=output_path+ os.sep + fileList[i]
        image = cv.imread(imagename)
        image = cv.resize(image, (480,360), interpolation=cv.INTER_LINEAR)
        cv.imwrite(outputname,image)

def findImgFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('_img.png'):
                fullname = os.path.join(root, f)
                yield fullname

def findLabelFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('_label.png'):
                fullname = os.path.join(root, f)
                yield fullname

def json_to_dataset(json_path):
    json_file = os.listdir(json_path) 
    # os.system("conda activate base") 
    for file in json_file: 
        os.system("labelme_json_to_dataset.exe %s"%(json_path + '/' + file))
    train_img_dir = '../Sweeper_Audit_Model/dataset/sweeper/train/'
    if not os.path.exists(train_img_dir):
        os.makedirs(train_img_dir)
    for i in findImgFile(json_path):
        shutil.copyfile(i,train_img_dir+i.split('\\')[-1])
    train_label_dir = '../Sweeper_Audit_Model/dataset/sweeper/train_labelme/'
    if not os.path.exists(train_label_dir):
        os.makedirs(train_label_dir)    
    for i in findLabelFile(json_path):
        shutil.copyfile(i,train_label_dir+i.split('\\')[-1])

if __name__ == "__main__":
    path='./images'
    output_path='./images'
    json_path = 'environment_configuration/raw_data_preprocess/clean' # path为json文件存放的路径 
    #获取该目录下所有文件，存入列表中
    need_change_name,need_image_process,need_json_to_dataset = True, True, False
    if need_change_name:
        change_name(2389, path)
    if need_image_process:
        image_preprocess(path,output_path)
    if need_json_to_dataset:
        json_to_dataset(json_path)


