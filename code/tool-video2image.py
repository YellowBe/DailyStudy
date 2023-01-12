import cv2
import shutil
import os
def video2img(input_path,outpath):
    cap = cv2.VideoCapture(input_path)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('总帧数：', total_frame)
    
    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    else:
        shutil.rmtree(outpath)
        os.makedirs(outpath)
    counter = 0
    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            counter += 1
            imgname = "%s.jpg"% str(counter)
            path = os.path.join(outpath, imgname)
            cv2.imwrite(path,frame)
            print(counter)
    cap.release()


if __name__ == "__main__":  
    video2img('1.mp4','images')