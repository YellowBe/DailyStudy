
# 2022.09.13
## 自己DIY conv2d函数
```
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
```




# 2022.9.30
## First, how to build the model in pytorch? / how is a model like in pytorch
+ in main func, define a func to return a model class
    ```
    model = build_model(args.model, num_classes=args.classes)
    def build model():
        return ERFNet()
    ```
## func in torch
+ nn.Conv2d
    +  Applies a 2D convolution over an input signal composed of several input planes / 对由多个输入平面组成的输入信号进行二维卷积
    + [Instruction](https://blog.csdn.net/qq_34243930/article/details/107231539)
# 2022.10.04
## UNet
### The structure of UNet
+ https://arxiv.org/pdf/1505.04597.pdf

# 2022.10.05
## structure
### nn.sequential
+ resource code of nn.sequential
+ https://blog.csdn.net/dss_dssssd/article/details/82980222
+ https://pytorch.org/docs/stable/_modules/torch/nn/modules/container.html#Sequential
#### how the nn.sequential call every layer of one module?
+ https://blog.csdn.net/dss_dssssd/article/details/82977170

# 2022.10.11
### maxpooling 及其作用
1. invariance(不变性)，这种不变性包括translation(平移)，rotation(旋转)，scale(尺度)
2. 保留主要的特征同时减少参数(降维，效果类似PCA)和计算量，防止过拟合，提高模型泛化能力
#### 平移不变性

# 2022.11.10
### pytorch中的reshape()、view()、transpose()和flatten()
https://blog.csdn.net/a1367666195/article/details/105600709
+ torch.reshape()
  + 其作用是在不改变tensor元素数目的情况下改变tensor的shape
+ torch.view()
  + view()和reshape()在效果上是一样的，区别是view（）只能操作contiguous的tensor，且view后的tensor和原tensor共享存储，reshape（）对于是否contiuous的tensor都可以操作。
+ torch.transpose()
  + 将输入数据input的第dim0维和dim1维进行交换
+ torch.flatten()
  + 其作用是将输入tensor的第start_dim维到end_dim维之间的数据“拉平”成一维tensor

### Droppath
+ DropPath 类似于Dropout，不同的是 Drop将深度学习模型中的多分支结构随机 “失效” 而Dropout 是对神经元随机 “失效”

# 2022.11.15
### python中的@
+ https://www.zhihu.com/question/36223283
+ 在python 3.5以后，@是一个操作符，表示矩阵-向量乘法, A@x 就是矩阵-向量乘法A*x: np.dot(A, x)