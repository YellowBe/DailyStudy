#!/usr/bin/env python3
#!coding:utf-8 

#function: 
#record video based on detect result and save into database.

from cv_bridge import CvBridge
import cv2
import os
import time
from geopy.geocoders import Nominatim
import pymysql
import paramiko
# import datetime

class ResultSave():
    def __init__(self):
        self.connection = pymysql.connect(host='192.168.0.126',
                             user='root',
                             password='123',
                             db='sweeper')
        self.create_path()
        self.bridge = CvBridge()
        self.vdname = self.starttime = self.endtime = ''
        self.starttime1=time.time()
        self.unclean_degree = 0
        self.max_unclean_degree = 0
        self.Order = 4
        self.lat=float(51.47688)
        self.lng=float(-0.0005)
        self.road=self.suburb=self.county=self.country="Unknown" 
        self.postcode = 111111
        self.videoWriter = cv2.VideoWriter()
        self.fps = 30
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')   
        self.vehicle_id = 'Sweeper1'
        self.query_table_sql = """\
        select * from home_total;
        """
        self.insert_table_sql = """\
        INSERT INTO home_total(vehicle_id,company,currentdate,currenttime,road,suburb,county,postcode,avg_unclean_level,duration,latitude,longitude)
        VALUES('{VehicleID}','{Company}','{Currentdate}','{Currenttime}','{Road}','{Suburb}','{County}','{Postcode}','{AvgUncleanLevel}','{Duration}','{Latitude}','{Longitude}')
        """
    def create_path(self):
        self.save_path = "~/data/"
        self.save_path = os.path.expanduser(self.save_path)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
    def avi_to_web_mp4(self, input_file_path):
        output_file_path = input_file_path[:-3] + 'mp4'
        cmd = 'ffmpeg -y -i {} -vcodec h264 {}'.format(input_file_path, output_file_path)
        os.system(cmd)
        return output_file_path
    def save_to_centerportal(self,duration,unclean_degree,currentdate,currenttime,vehicle_id,latitude,longitude,road,suburb,county,postcode):
        """
        This function save the details information about video into datafile.
        """ 
        # try:
        with self.connection.cursor() as cursor:
            cursor.execute(
                self.insert_table_sql.format(VehicleID='Sweeper1',Company='NTU',Currentdate=currentdate,Currenttime=currenttime,Road=road,Suburb=suburb,County=county,Postcode=postcode,AvgUncleanLevel=unclean_degree,Duration=duration,Latitude=latitude,Longitude=longitude))
            self.connection.commit()
            cursor.execute(self.query_table_sql)
            results = cursor.fetchall()
        tran = paramiko.Transport(('192.168.0.126', 22))
        tran.connect(username="NTU-NUC2", password='Ntu123456')
        sftp = paramiko.SFTPClient.from_transport(tran)
        savefolder = "~/data/"
        savefolder = os.path.expanduser(savefolder)
        savevideopath = savefolder + vehicle_id + '_' + currentdate+'-'+currenttime +'.avi'
        savevideopath = self.avi_to_web_mp4(savevideopath)
        saveimgpath = './display_image/seg_image.png'

        remotefolder = r'C:/Users/NTU-NUC2/sweeper_audit/environment_configuration/command_center/sweeper_command_center/home/static/home/data/'
        remotevideopath = remotefolder + vehicle_id + '_' + currentdate+'-'+currenttime +'.mp4'
        remoteimgpath = remotefolder + vehicle_id + '_' + currentdate+'-'+currenttime +'.png'
        sftp.put(savevideopath, remotevideopath)
        sftp.put(saveimgpath, remoteimgpath)
        tran.close()

    def callback_1(self,data):
        fps = self.fps
        fourcc = self.fourcc
        img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        # size = (int(img.shape[1]),
        #         int(img.shape[0]))
        size = (800,600)
        img= cv2.resize(img, size, interpolation=cv2.INTER_LINEAR)
        #Judging recording conditions
        if self.Order==1:
            self.currentdate = time.strftime('%m-%d-%Y', time.localtime())
            self.currenttime = time.strftime('%H-%M-%S', time.localtime())
            self.vdname = self.vehicle_id+'_%s.avi' % (self.currentdate+'-'+self.currenttime)
            self.starttime=time.strftime("%H:%M:%S",time.localtime())
            self.starttime1=time.time()
            self.videoWriter.open(self.save_path+self.vdname,fourcc,fps,size,True)
            self.videoWriter.write(img)
            self.Order=2
        elif self.Order==2:
            self.videoWriter.write(img)
        elif self.Order==3:
            self.videoWriter.release()
            self.endtime=time.strftime("%H:%M:%S",time.localtime())
            duration=int(time.time()-self.starttime1)
            print('unclean degree = ' + str(self.unclean_degree))
            if self.unclean_degree>=3 and duration>=3:
                self.save_to_centerportal(duration,self.unclean_degree,self.currentdate,self.currenttime,self.vehicle_id,self.lat,self.lng,self.road,self.suburb,self.county,self.postcode)
                self.unclean_degree = 1
            if os.path.exists(self.save_path+self.vdname):
                os.remove(self.save_path+self.vdname)
            if os.path.exists((self.save_path+self.vdname)[:-3]+'mp4'):
                os.remove((self.save_path+self.vdname)[:-3]+'mp4')
            self.Order=4

    def callback_2(self,data):
        self.Order = data.data

    def callback_3(self,data):
        self.unclean_degree = data.data
    #===============================gps signal to address===================
    def callback_4(self,message):
        self.lat = message.latitude
        self.lng = message.longitude
        #rospy.loginfo("latitude is  %f, longtitude is %f ", lat, lng)
        if str(self.lat)!="nan" and str(self.lng)!="nan":
            locstr = str(self.lat) + ", " +  str(self.lng) 
            geoLoc = Nominatim(user_agent = "getloc")
            # passing the coordinates
            address = geoLoc.reverse(locstr).address
            [_,self.road,self.suburb,self.county,self.postcode,self.country] = address.split(", ")

        else:
            self.road=self.suburb=self.county=self.country = "Unknown"
            self.postcode= 111111
            self.lat=float(51.47688)
            self.lng=float(-0.0005)
        # print(self.road,self.suburb,self.country,self.postcode,self.lat,self.lng)

if __name__ == '__main__':
    ResultSave().callback_1()
