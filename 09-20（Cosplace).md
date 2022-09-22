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