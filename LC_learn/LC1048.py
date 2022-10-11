class Solution:
    def longestStrChain(self, words) -> int:
        def check(x,y):
            m,n = len(x),len(y)
            if m+1 != n:return False
            i,j = 0,0
            while i<m and j<n:
                if x[i] == y[j]:i+=1
                j += 1
            return i == len(x) 

        words.sort(key = lambda x : len(x))
        n = len(words)
        dp = [1]*n
        res = 0
        for i in range(n):
            for j in range(i):
                if check(words[j],words[i]):
                    dp[i] = max(dp[i],dp[j]+1)
            res = max(res,dp[i])
        return res

class Solution:
    def longestStrChain(self, words) -> int:
        def check(x,y):
            m,n = len(x),len(y)
            if m+1 != n:return False
            i,j = 0,0
            while i < m and j < n:
                if x[i]==y[j]: i+=1
                j+=1
            return i == len(x)
        
        words.sort(key = lambda x : len(x))
        n = len(words)
        dp = [1] * n
        res = 0
        for i in range(n):
            for j in range(i):
                if check(words[j],words[i]):
                    dp[i] = max(dp[i],dp[j]+1)
                res = max(res,dp[i])
        return res

class Solution:
    def longestStrChain(self, words) -> int:
        def check(x,y):
            m,n = len(x),len(y)
            if m+1 != n:return False
            i,j =0,0
            while i<m and j<n:
                if x[i]==y[j]: i+=1
                j+=1
            return i ==len(x)

        words.sort(key = lambda x : len(x))
        n = len(words)
        dp = [1] * n
        res = 0
        for i in range(n):
            for j in range(i):
                if check(words[j],words[i]):
                    dp[i] = max(dp[i],dp[j]+1)
                res = max(res,dp[i])
        return res

if __name__ == "__main__":
    result = Solution()
    ans = result.longestStrChain(["a","b","ba","bca","bda","bdca"])
    print(ans)