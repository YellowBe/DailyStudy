# 给定一个二叉树和一个目标和，判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和。

# 说明: 叶子节点是指没有子节点的节点。

# 如果需要搜索整棵二叉树且不用处理递归返回值，递归函数就不要返回值。（这种情况就是本文下半部分介绍的113.路径总和ii）
# 如果需要搜索整棵二叉树且需要处理递归返回值，递归函数就需要返回值。 （这种情况我们在236. 二叉树的最近公共祖先 (opens new window)中介绍）
# 如果要搜索其中一条符合条件的路径，那么递归一定需要返回值，因为遇到符合条件的路径了就要及时返回。（本题的情况）
class solution:
    def haspathsum(self, root: treenode, targetsum: int) -> bool:
        def isornot(root, targetsum):
            if (not root.left) and (not root.right) and targetsum == 0:
                return True
            if (not root.left) and (not root.right):
                return False
            if root.left:
                targetsum -= root.left.val # 计算
                if isornot(root.left, targetsum): return True # 递归， 处理左节点
                targetsum += root.left.val # 还原到上一状态，需要回溯，还原递归之前的处理条件
            if root.right:
                targetsum -= root.right.val
                if isornot(root.right, targetsum): return True
                targetsum += root.right.val
            return False

        if root == None:
            return False
        else:
            return isornot(root, targetsum - root.val)


# LC113
class solution:
    def pathsum(self, root: treenode, targetsum: int) -> list[list[int]]:

        def traversal(cur_node, remain): 
            if not cur_node.left and not cur_node.right:
                if remain == 0: 
                    result.append(path[:])
                return

            if cur_node.left: 
                path.append(cur_node.left.val)
                traversal(cur_node.left, remain-cur_node.left.val)
                path.pop()

            if cur_node.right: 
                path.append(cur_node.right.val)
                traversal(cur_node.right, remain-cur_node.left.val)
                path.pop()

        result, path = [], []
        if not root: 
            return []
        path.append(root.val)
        traversal(root, targetsum - root.val)
        return result

# 不给return的话会走完整个函数