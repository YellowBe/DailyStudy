class Solution:
    def __init__(self):
        self.path = []
        self.paths = []
    def permute(self, nums):
        usage_list = [False] * len(nums)
        self.backtracking(nums,usage_list)
        return self.paths
    
    def backtracking(self, nums, usage_list):
        if len(self.path)==len(nums):
            self.paths.append(self.path[:])
            return
        
        for i in range(0, len(nums)):
            if usage_list[i] == True:
                continue
            usage_list[i] = True
            self.path.append(nums[i])
            self.backtracking(nums, usage_list)
            self.path.pop()
            usage_list[i] = False


class Solution:
    def __init__(self):
        self.path = []
        self.paths = []

    def permute(self, nums: List[int]) -> List[List[int]]:
        '''
        因为本题排列是有序的，这意味着同一层的元素可以重复使用，但同一树枝上不能重复使用
        所以处理排列问题每层都需要从头搜索，故不再使用start_index
        '''
        self.backtracking(nums)
        return self.paths
    def backtracking(self, nums):
        if len(self.path) == len(nums):
            self.paths.append(self.path[:])
            return
        
        for i in range(0,len(nums)):
            if nums[i] in self.path:
                continue
            self.path.append(nums[i])
            self.backtracking(nums)
            self.path.pop()


