import rospy
from sensor_msgs.msg import Image, NavSatFix 
from std_msgs.msg import Int8, Float32
from tools.detect import RosPublish
from tools.save import ResultSave
import pymysql

if __name__ == '__main__':
    rospy.init_node('sweeper', anonymous=True)
    detect_node = RosPublish()
    save_node = ResultSave()
    rospy.Subscriber('/camera/image_color', Image, detect_node.callback) #/galaxy_camera/image_raw      /camera/image_color  /hikrobot_camera/rgb
    rospy.Subscriber('/camera/image_color', Image, save_node.callback_1) #/image_view/image_raw /camera/image_color /hikrobot_camera/rgb
    rospy.Subscriber('/signal', Int8, save_node.callback_2)
    rospy.Subscriber('/unclean_percent', Int8, save_node.callback_3)
    rospy.Subscriber("/fix", NavSatFix, save_node.callback_4)
    rospy.spin()
    connection = pymysql.connect(host='192.168.0.126',
                             user='root',
                             password='123',
                             db='sweeper')
    connection.close()