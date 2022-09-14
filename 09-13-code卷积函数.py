from math import floor
import numpy as np
# print('请输入卷积核信息：')
# kernel_msg=input()
kernel_msg = '3 3, 1 2 1 2 4 2 1 2 1'
kernel_sz=kernel_msg.split(',')[0]
kernel_ele=kernel_msg.split(',')[1]
m,n=int(kernel_sz.split()[0]),int(kernel_sz.split()[1])
kernel_ele=kernel_ele.split()
lst=[int(x) for x in kernel_ele]
kernel=np.array(lst)
kernel=kernel.reshape(m,n)
# print(kernel.shape[0])
 
# print('请输入图片信息：')
# img_msg=input()
img_msg = '5 5, 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1'
img_sz=img_msg.split(',')[0]
img_ele=img_msg.split(',')[1]
img_m,img_n=int(img_sz.split()[0]),int(img_sz.split()[1])
img_ele=img_ele.split()
lst=[int(x) for x in img_ele]
img=np.array(lst)
img=img.reshape(img_m,img_n)
 
# print('请输入步长信息：')
# stride=int(input())
stride = 1
 
def conv2d(kernel,img,stride=1):
    m,n=kernel.shape[0],kernel.shape[1]
    padding_m=floor(m/2)
    padding_n=floor(n/2)
    img_m,img_n=img.shape[0],img.shape[1]
    zero_mat=np.zeros((img_m+2*padding_m,img_n+2*padding_n))
    zero_mat[padding_m:padding_m+img_m,padding_n:padding_n+img_n]=img
    img=zero_mat
    conv_res=np.zeros(((zero_mat.shape[0] - m) // stride + 1, (zero_mat.shape[1] - n) // stride + 1))
    for i in range(0, img.shape[0]-m+1, stride):
        for j in range(0, img.shape[1]-n+1, stride):
            val = np.sum(kernel * img[i: i + m, j: j + n])
            conv_res[i // 2][j // 2] = val 
    return conv_res
conv_res=conv2d(kernel, img, stride)
lst=conv_res.tolist()
lst=[_ for item in lst for _ in item]
res='{} {},'.format(conv_res.shape[0],conv_res.shape[1])
for i in lst:
    res+=' '+str(int(i))
print(res)