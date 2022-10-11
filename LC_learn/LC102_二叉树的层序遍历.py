class Solution:
    def leverOrder(self, root):
        results = []
        if not root:
            return results

        from collections import deque
        que = deque([root])

        while que:
            size =len(que)
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


class Solution:
    """N叉树的层序遍历迭代法"""
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        results = []
        if not root:
            return results
        
        from collections import deque
        que = deque([root])

        while que:
            result = []
            for _ in range(len(que)):
                cur = que.popleft()
                result.append(cur.val)
                # cur,children 是 Node对象组成的列表，也可能为None
                if cur.children:
                    que.extend(cur.children)
            results.append(result)

        return results
        