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

## Loss
+ Triplet Margin Loss
  + https://pytorch.org/docs/stable/generated/torch.nn.TripletMarginLoss.html#torch.nn.TripletMarginLoss
+ torch.bmm()
  + https://blog.csdn.net/qq_40178291/article/details/100302375
  + 计算两个tensor的矩阵乘法，torch.bmm(a,b),tensor a 的size为(b,h,w),tensor b的size为(b,w,m) 也就是说两个tensor的第一维是相等的，然后第一个数组的第三维和第二个数组的第二维度要求一样，对于剩下的则不做要求，输出维度 （b,h,m）
+ Smooth L1 Loss (Huber loss)
  + https://pytorch.org/docs/stable/generated/torch.nn.SmoothL1Loss.html