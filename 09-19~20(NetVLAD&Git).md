## Git 回滚代码
+ https://zhuanlan.zhihu.com/p/137856034

## Git 小技巧
+ https://www.zhihu.com/question/20866683/answer/711725573
+ ```git reflog```
+ 这条命令能列出你在 Git 上的所有操作记录，你只要找到 HEAD@{index} 前面所对应的操作索引.
+ ```git reset HEAD@{index}```
+ 回退

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