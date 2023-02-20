# 404 左叶子节点之和
class Solution:
    def sumOfLeftLeaves(self, root):
        if not root:
            return 0
        
        left_left_leaves_sum = self.sumOfLeftLeaves(root.left)
        right_left_leaves_sum = self.sumOfLeftLeaves(root.right)

        cur_left_leaf_val = 0
        if root.left and not root.left.left and not root.left.right:
            cur_left_leaf_val = root.left.val
        return cur_left_leaf_val + left_left_leaves_sum + right_left_leaves_sum # 中
