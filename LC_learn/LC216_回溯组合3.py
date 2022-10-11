class Solution:
    def __init__(self):
        self.res = []
        self.sum_now = 0
        self.path = []
    def combinationSum3(self, k, n):
        self.backtracking(k,n,1)
        return self.res
    
    def backtracking(self, k, n, start_num):
        if self.sum_now > n:
            return
        if len(self.path) == k:
            if self.sum_now == n:
                self.res.append(self.path[:])
            return
        for i in range(start_num, 10-(k-len(self.path))+1):
            self.path.append(i)
            self.sum_now += i 
            self.backtracking(k, n, i+1)
            self.path.pop()
            self.sum_now -= i