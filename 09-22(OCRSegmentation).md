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