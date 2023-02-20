# 层序遍历
class Solution:
    def levelOrder(self, root):
        results = []
        if not root:
            return results
        from collections import deque
        que = deque([root])

        while que:
            size = len(que)
            result = []
            for _ in range(size):
                cur = que.popleft()
                result.append(cur.val)
                if cur.left:
                    que.append(cur.left)
                if cur.right:
                    que.append(cur.right)
            results.append(result)

        return results

# 翻转二叉树
# 递归法前序遍历
# Python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return None
        root.left, root.right = root.right, root.left #中
        self.invertTree(root.left) #左
        self.invertTree(root.right) #右
        return root

// C++
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (root == NULL) return root;
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};

# // 二叉树的最大深度
# // python
class solution: #左右中
    def getdepth(self, node):
        if not node:
            return 0
        leftheight = self.getdepth(node.left)
        rightheight = self.getdepth(node.right)
        height = 1 + max(leftheight, rightheight)
        return height
    def maxdepth(self, root):
        return self.getdepth(root)

# 前序遍历， dfs
# C++
class solution {
public:
    int result;
    void getdepth(treenode* node, int depth){
        result = depth > result ? depth : result; //中
    if (node->left == NULL && node->right == NULL) return ;

    if (node->left) { // 左
        depth++;
        getdepth(node->left, depth);
        depth--;
    }
    if (node->right){
        depth++;
        getdepth(node->right, depth);
        depth--;
    }
    return ;
    }
    int maxdepth(treenode* root) {
        result = 0;
        if (root == NULL) return result;
        getdepth(root, 1);
        return result;
    }
};

// 求二叉树最小深度(处理左右孩子不为空)
class Solution {
public:
    int getDepth(TreeNode* node) {
        if (node == NULL) return 0;
        int leftDepth = getDepth(node->left);
        int rightDepth = getDepth(node->right);

        // 当一个左子树为空，右不为空，这时并不是最低点
        if (node->left == NULL && node->right != NULL) {
            return 1 + rightDepth;
        }

        // 当一个右子树为空，左不为空，这时并不是最低点
        if (node->left != NULL && node->right == NULL) {
            return 1 + leftDepth;
        }
        int result = 1 + min(leftDepth, rightDepth);
        return result;
    }

    int minDepth(TreeNode* root) {
        return getDepth(root);
    }
}

class Solution:
    def minDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        
        min_depth = 10**9
        if root.left:
            min_depth = min(self.minDepth(root.left), min_depth)
        if root.right:
            min_depth = min(self.minDepth(root.right), min_depth)
        return min_depth + 1