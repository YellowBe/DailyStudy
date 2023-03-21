#!/usr/bin/env python3
#!coding=utf-8
##function: 
#detect the cleanness of each frame.
import rospy
from std_msgs.msg import Int8, Float32
import cv2
from cv_bridge import CvBridge
import os
import numpy as np
# from PIL import Image as Img
import torch
# from torch.autograd import Variable as V
# import torchvision.models as models
# from torchvision import transforms as trn
# import torchvision.transforms as transforms
# from torch.nn import functional as F
import torch.backends.cudnn as cudnn
from MODELS.CGNet import CGNet
import matplotlib


 
# def cleanness_monitoring(image, arch, model_file = '/home/ljw/catkin_ws/src/image_get/scripts/checkpoints/Sweeper_18_model_best.pth.tar'):
#     T1 = time.time()
#     device = torch.device("cuda")#cuda cpu
#     # load the pre-trained weights

#     #if not os.access(model_file, os.W_OK):
#     #    print('no weight file')
#     # model = models.__dict__['vgg16'](num_classes=2)
#     if arch == "Resnet_CBAM":
#         model = ResidualNet( 'CIFAR10', 18, 2, 'CBAM')
#     else:
#         model = create_model(arch, num_classes=2)
#     T2 = time.time()
#     print('load_model time is %ss' % (T2 - T1))
#     checkpoint = torch.load(model_file, map_location=lambda storage, loc: storage)
#     # print(' ====#On epoch {0} resnet18 has best train Prec@1 {trntop1:.3f} and test Prec@1 {valtop1:.3f}#===='#+CBAM
#     #             .format(checkpoint['epoch'],trntop1=checkpoint['best_traprec1'], valtop1=checkpoint['best_valprec1']))
#     pretrained_dict = checkpoint['state_dict']
#     model_dict = {str.replace(k,'module.',''): v for k, v in model.state_dict().items()} # Debug: added on 2021/6/25
#     # 1. filter out unnecessary keys
#     pretrained_dict = {str.replace(k,'module.',''): v for k, v in pretrained_dict.items() if str.replace(k,'module.','') in model_dict and model_dict[str.replace(k,'module.','')].shape== pretrained_dict[k].shape}
#     # 2. overwrite entries in the existing state dict
#     #print('=> params of {} will be loaded'.format(pretrained_dict.keys()))
#     model_dict.update(pretrained_dict) 
#     # 3. load the new state dict
#     print("=> loaded weights")
    
#     model = model.to(device)
#     # load the image transformer
#     centre_crop = trn.Compose([
#             trn.Resize(256),
#             trn.CenterCrop(224),
#             transforms.ColorJitter(contrast=[1,2]),
#             trn.ToTensor(),
#             trn.Normalize(mean=[0.5984, 0.5953, 0.5602], std=[0.1596,  0.1553, 0.1612]) #([0.485, 0.456, 0.406], [0.5, 0.5, 0.5])
#     ])
#     #file_name = 'categories.txt'
#     # categories.txt includes:
#     #‘’‘/clean 0
#     #   /not_clean 1‘’‘
#     #classes = list()
#     #with open(file_name) as class_file:
#     #    for line in class_file:
#     #        classes.append(line.strip().split(' ')[0][1:])#
#     #classes = tuple(classes)
#     #print(classes)

#     img = centre_crop(image.convert('RGB')).unsqueeze(0)
#     input_img = V(img.to(device))

#     model.eval()
#     logit = model.forward(input_img)
#     h_x = F.softmax(logit, 1).data.squeeze()
#     # #output = model(input).detach_()
#     probs, idx = h_x.sort(0, True)
#     #idx[0]=0,clean;idx[0]=1 notclean
#     return (idx[0]).cpu().numpy()

 


class Detection():
    def __init__(self) -> None:
        matplotlib.use('Agg')
        self.seg_model = CGNet(classes=4)
    def cuda_detect(self,cuda,gpus):
        if cuda:
            device = torch.device("cuda")
            os.environ["CUDA_VISIBLE_DEVICES"] = gpus
            if not torch.cuda.is_available():
                raise Exception("no GPU found or wrong gpu id, please run without --cuda")
        else:
            device = torch.device("cpu")
        return device
    
    def model_evaluation(self,model,checkpoint_path,device):
        cudnn.benchmark = True
        if checkpoint_path:
            if os.path.isfile(checkpoint_path):
                checkpoint = torch.load(checkpoint_path, map_location=device)
                model.load_state_dict(checkpoint['model'])
            else:
                raise FileNotFoundError("no checkpoint found at '{}'".format(checkpoint_path))
        return model

    def image_augmentation(self,predict_image):
        image = cv2.cvtColor(predict_image, cv2.IMREAD_COLOR)
        dim = (480,360)
        mean=(89.02598,91.51838,91.355064) #(115.20707,115.52273,115.017975) #mean=(117.64809,123.275635,124.548775)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        image = np.asarray(image, np.float32)
        image -= mean
        image = image[:, :, ::-1]  # revert to RGB
        image = image.transpose((2, 0, 1))  # HWC -> CHW
        output_image = image.copy()
        output_image = torch.from_numpy(output_image).unsqueeze(0)
        return output_image

    def cal_unclean_degree(self,seg_output):
        output = seg_output.cpu().data[0].numpy()
        output = output.transpose(1, 2, 0)
        output = np.asarray(np.argmax(output, axis=2), dtype=np.uint8)
        label_output = output.copy()
        try:
            rate_trash_road = np.sum(output==3)/(np.sum(output==1)+np.sum(output==3))
        except:
            print('image error')
        if rate_trash_road >= 0.01 and rate_trash_road!=float("inf"):
            seg_clean = 0
            if 0.01 <= rate_trash_road < 0.02:
                unclean_degree = 1
            elif 0.02 <= rate_trash_road < 0.05:
                unclean_degree = 2
            elif 0.05 <= rate_trash_road < 0.1: 
                unclean_degree = 3
            elif rate_trash_road > 0.1: 
                unclean_degree = 4
                
        else:
            seg_clean = 1
            unclean_degree = 0
        return unclean_degree,rate_trash_road,seg_clean,label_output

    def uncleanimage_save(self,input_image,label_output,unclean_degree):
        _,thresh = cv2.threshold(label_output,2,255,cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
        input_image = cv2.resize(input_image,(480,360), interpolation=cv2.INTER_LINEAR)
        cv2.drawContours(input_image,contours,-1,(0,0,255),2)
        try:
            # cv2.namedWindow("segmentation", 0)
            # cv2.resizeWindow("segmentation", 1920, 1080)
            # cv2.moveWindow("segmentation", 1300, 0)
            # cv2.imshow("segmentation", input_image)
            cv2.imwrite('./display_image/seg_image.png',input_image)
            cv2.waitKey(1)
        except KeyboardInterrupt:
            raise        
        except Exception:
            pass        

    def prediction(self, predict_image, cuda = True, gpus = "0",checkpoint_path = ''):
        pub2 = rospy.Publisher('/unclean_percent', Int8, queue_size=1)

        device = self.cuda_detect(cuda,gpus)
        model = self.model_evaluation(self.seg_model,checkpoint_path,device)
        image = self.image_augmentation(predict_image)

        model.eval()
        model = model.to(device)
        with torch.no_grad():
            input_var = image.to(device)
        seg_output = model(input_var)
        unclean_degree,rate_trash_road,seg_clean,label_output = self.cal_unclean_degree(seg_output)
        if rate_trash_road >= 0.01 and rate_trash_road!=float("inf"):
            print(rate_trash_road)
            # print('now the rate_trash_road = ' + str(rate_trash_road))
            if 0.01 <= rate_trash_road < 0.02:
                unclean_degree = 1
            elif 0.02 <= rate_trash_road < 0.05:
                unclean_degree = 2
            elif 0.05 <= rate_trash_road < 0.1: 
                unclean_degree = 3
                self.uncleanimage_save(predict_image,label_output,unclean_degree)
            elif 0.1 <= rate_trash_road < 0.4: 
                unclean_degree = 4
                self.uncleanimage_save(predict_image,label_output,unclean_degree)
            elif 0.4 <= rate_trash_road: 
                unclean_degree = 5
                self.uncleanimage_save(predict_image,label_output,unclean_degree)
            if unclean_degree >= 3: 
                pub2.publish(unclean_degree)
        # T2 = time.time()
        # print('segmentation inference time is %ss' % (T2 - T1))

        return seg_clean #,temp_image


class RosPublish():
    def __init__(self) -> None:
        self.clean_r = 1
        self.r0 = 1
        self.det_interval = 20
        self.bridge = CvBridge()
        self.count = 0
    def callback(self,data):
        self.count = self.count + 1
        pub1 = rospy.Publisher('/signal', Int8, queue_size=1)
        cv_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        if self.count == self.det_interval:
            self.count = 0
            # This place con't be data.data, or it will be str_type
            # cleanness segmentation
            seg_clean = Detection().prediction(
                predict_image= cv_img,
                cuda = True,
                checkpoint_path= './checkpoints/CGNET_model_291.pth')
            # cleanness classification      
            # img_arr = Img.fromarray(temp_image)
            # T3 = time.time()    
            # cls_clean = cleanness_monitoring(
            #     img_arr,
            #     'Resnet_CBAM',)
                # '/home/ljw/cleanness/cleanness1/output/train/20220408-112422-mnasnet_small-224/Sweeper_mnasnet_small_model_best.pth.tar')
            # T4 = time.time()
            # print('classification inference time is %ss' % (T4 - T3))
            # combine seg result and cls result
            self.clean_r = seg_clean #+ cls_clean
            #-----------------------------------
            if self.r0 == 1 and self.clean_r==0:
                x=1
            elif self.r0==0 and self.clean_r==0:
                x=2
            elif self.r0==0 and self.clean_r!=0:
                x=3
            else:
                x=4
            #print(r0, clean_r)
            pub1.publish(x)
            if x != 4:
                rospy.loginfo("Publish order message to save node[%d]", x)
            self.r0 = self.clean_r
        else:
            pass
 
    # def ros_eval(self):
    #     rospy.init_node('detection', anonymous=True)
    #     # make a video_object and init the video object
    #     rospy.Subscriber('/camera/image_color', Image, self.callback)#/galaxy_camera/image_raw      /camera/image_color  /hikrobot_camera/rgb
    #     rospy.spin()
if __name__ == '__main__':
    RosPublish().ros_eval()
