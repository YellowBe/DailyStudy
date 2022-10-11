# 组合问题：N个数里按一定规则找出k个数的集合
# 切割问题：一个字符串按一定规则有几种切割方式
# 子集问题：一个N个数的集合里有多少符合条件的子集
# 排列问题：N个数按一定规则全排列，有几种排列方式
# 棋盘问题：N皇后等
class Solution(object):
    def combine(self, n, k):
        res = []
        path = []
        def backtrack(n, k, StartIndex):
            if len(path) == k:
                res.append(path[:])
                return
            for i in range(StartIndex, n + 1): #for循环是横向遍历
                path.append(i)
                backtrack(n, k, i+1) #递归是纵向遍历
                path.pop()
        backtrack(n, k, 1)
        return res


class Solution(object):
    def combine(self, n, k):
        res = []
        path = []
        def backtrack(n,k,StartIndex):
            if len(path) == k:
                res.append(path[:])
                return
            for i in range(StartIndex, n+1):
                path.append(i)
                backtrack(n,k,i+1)
                path.pop()
        backtrack(n,k,1)
        return res


if __name__ == "__main__":
    result = Solution()
    ans = result.combine(4,2)
    print(ans)            
#剪枝版本
class Solution(object):
    def combine(self, n, k):
        res = []
        path = []
        def backtrack(n,k,startIndex):
            if len(path) == k:
                res.append(path[:])
                return
            for i in range(startIndex, n-(k-len(path))+2):
                path.append(i)
                backtrack(n,k,i+1)
                path.pop()
        backtrack(n,k,1)
        return res