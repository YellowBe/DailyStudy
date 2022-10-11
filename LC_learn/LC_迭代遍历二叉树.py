from pickletools import stackslice


class Solution:
    def preorderTraversal(self, root) -> List[int]:
        if not root:
            return []
        stack = [root]
        result = []
        while stack:
            node = stack.pop()
            result.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

class Solution:
    def inorderTraversal(self, root):
        if not root:
            return []
        stack = []
        result = []
        cur = root
        while cur or stack:
            if cur:
                stack.append(cur)
                cur = cur.left
            # 到达最左结点后处理栈顶结点
            else:
                cur = stack.pop()
                result.append(cur.val)
                # 取栈顶元素右结点
                cur = cur.right
        return result

class Solution:
    def postorderTraversal(self,root):
        if not root:
            return []
        stack = [root]
        result = []
        while stack:
            node = stack.pop()
            # 中结点先处理
            result.append(node.val)
            # 左孩子先入栈
            if node.left:
                stack.append(node.left)
            # 右孩子后入栈
            if node.right:
                stack.append(node.right)
        # 将最后数组翻转
        return result[::-1]