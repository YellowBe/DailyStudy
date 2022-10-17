
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
# 2022.09.16
## Paper
### CosPlace
+ VPR with classification
### NetVLAD
+ NetVLAD, inspired by the Vector of Locally Aggregated Descriptors (VLAD) representation [29] that has shown excellent performance in image retrieval and place recognition. The layer is readily pluggable into any CNN architecture and amenable to training via backpropagation. The resulting aggregated representation is then compressed using Principal Component Analysis (PCA) to obtain the final compact descriptor of the image.
+ NetVLAD，受局部聚合描述符向量(VLAD)表示[29]的启发，在图像检索和位置识别方面表现出出色的性能。该层很容易插入到任何CNN架构中，并通过反向传播进行训练。然后使用主成分分析(PCA)对生成的聚合表示进行压缩，以获得图像的最终压缩描述符。
+ 这通常是通过设计一个函数f作为“图像表示提取器”来实现的，这样给定一个图像Ii，它产生一个固定大小的向量f(Ii)。
+ 在测试时，根据f(q)和f(Ii)之间的欧氏距离d(q, Ii)对图像进行排序，通过精确或快速近似最近邻搜索，找到与查询最接近的数据库图像，从而执行视觉搜索。
+ 它捕获关于聚合在图像上的本地描述符的统计信息。视觉词袋聚合保留视觉词的计数，而VLAD存储每个视觉词的残差之和(描述符与其相应聚类中心之间的差向量)。
+ 监督VLAD的好处。红色和绿色的圆圈是来自两个不同图像的局部描述符，分配到同一个集群(V oronoi cell)。在VLAD编码下，它们对两个图像之间的相似度评分的贡献是对应残差之间的标量积(因为最终的VLAD向量是l2归一化的)，其中残差向量被计算为描述符和集群锚点之间的差。锚点ck可以解释为特定聚类k局部新坐标系的原点。在标准VLAD中，锚点被选为聚类中心(×)，以便在数据库中均匀分布残差。然而，在有监督的设置中，当两个描述符已知属于不应该匹配的图像时，有可能学习一个更好的锚点(?)，它使新残差之间的标量积很小。
+ 以端到端的方式学习它的参数来完成VPR
  + 从谷歌街景时间机器中获取大量描述相同地点的弱标签图像。
    + 每个透视图像都标有源全景图的GPS位置。因此，两张地理上近距离的透视图像不一定描绘相同的物体，因为它们可能面向不同的方向或可能发生遮挡(例如，两张图像彼此在一个角落)，等等。
  + 设计了一种新的弱监督三元排序损失函数
    + 也就是说，对于给定的测试查询图像q，目标是将来自近处的数据库图像Ii * *的排名高于数据库中所有其他远处的图像Ii。换句话说，我们希望查询q和近处图像Ii * *之间的欧氏距离dθ(q, I)小于数据库Ii中到远处图像的距离。dθ(q, Ii *) < dθ(q, Ii)，对于所有图像Ii在地图上与查询的距离大于一定距离。
    + 
# 2022.9.20
## CosPlace
### Splitting the dataset into classes
+ A naive approach to divide the database into classes would be to split it into square geographical cells (see Fig. 3), using UTM coordinates {east, north}1, and further slice each cell into a set of classes according to each image’s orientation/heading {heading}.
+ 将数据库划分为类的一种简单方法是将其划分为正方形的地理单元格(见图3)，使用UTM坐标{东，北}1，并根据每张图像的方向/朝向{heading}进一步将每个单元格划分为一组类。
  + heading 在6Dof里意指朝向
+ Property 1: each class belongs to exactly one group.
+ Property 2: within a given group, if two images belong to different classes they are at least M · (N − 1) meters apart or α · (L − 1) degrees apart (see Fig. 4); Property 3: the total number of CosPlace Groups is N × N × L.
+ Property 4: no two adjacent classes can belong to the same group (unless N = 1 or L = 1).
+ 性质1:每个类只属于一个组。
+ 性质2:在给定的组内，如果两幅图像属于不同的类，则它们之间的距离至少为M·(N−1)米或α·(L−1)度(见图4);性质3:CosPlace组总数为N × N × L。
+ 性质4:相邻的两个类不能属于同一组(除非N = 1或L = 1)。
# 2022.9.22
## Segmentation Transformer: Object-Contextual Representations for Semantic Segmentation
+ Semantic segmentation is a problem of assigning one label li to each pixel pi of an image I, where li is one of K different classes.
+ 语义分割是给图像I的每个像素pi分配一个标签li的问题，其中li是K个不同类中的一个

## 全卷积网络FCN Fully Convolutional Networks for Semantic Segmentation
+ https://zhuanlan.zhihu.com/p/30195134

## 语义分割之MIoU原理与实现
+ https://www.jianshu.com/p/42939bf83b8a

## Loss
+ Triplet Margin Loss
  + https://pytorch.org/docs/stable/generated/torch.nn.TripletMarginLoss.html#torch.nn.TripletMarginLoss
+ torch.bmm()
  + https://blog.csdn.net/qq_40178291/article/details/100302375
  + 计算两个tensor的矩阵乘法，torch.bmm(a,b),tensor a 的size为(b,h,w),tensor b的size为(b,w,m) 也就是说两个tensor的第一维是相等的，然后第一个数组的第三维和第二个数组的第二维度要求一样，对于剩下的则不做要求，输出维度 （b,h,m）
+ Smooth L1 Loss (Huber loss)
  + https://pytorch.org/docs/stable/generated/torch.nn.SmoothL1Loss.html
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

# 2022.10.12
## 更直观的理解就是，Encoder负责将一张图片的每个像素点，通过复杂的计算过程，映射到某一个高维分布上，而Decoder则是负责将这个高维分布，映射到给定的类别区域。中间的高维分布，是我们不可见的，但神经网络却可以很好的使用它。正是这种借助中间的高维分布的思想，搭建起来了原图像到像素级分类图像的桥梁，实现了end-to-end的训练过程。

## ERFNet https://blog.csdn.net/baidu_23388287/article/details/102911321
### 1.开始先减少图片的size，减少冗余，并使用残差block来减小网络尺寸
### 模型沿用了Encoder-Decoder的结构
+ non_bottleneck 借鉴了resblock
  + ```         output = self.conv3x1_1(input)
        output = F.relu(output)
        output = self.conv1x3_1(output)
        output = self.bn1(output)
        output = F.relu(output)

        output = self.conv3x1_2(output)
        output = F.relu(output)
        output = self.conv1x3_2(output)
        output = self.bn2(output)

        if (self.dropout.p != 0):
            output = self.dropout(output)
        return F.relu(output+input)
    ```
## HRNet
+ https://github.com/HRNet/HRNet-Semantic-Segmentation/tree/HRNet-OCR?v=2
+ paper: https://arxiv.org/pdf/1909.11065v6.pdf