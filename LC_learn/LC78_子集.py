class Solution:
    def __init__(self):
        self.path = []
        self.paths = []

    def subsets(self, nums):
        self.paths.clear()
        self.path.clear()
        self.backtracking(nums, 0)
        return self.paths

    def backtracking(self, nums, start_index) -> None:
        # 收集子集，要先于终止判断
        self.paths.append(self.path[:])
        # Base Case
        if start_index == len(nums):
            return

        # 单层递归逻辑
        for i in range(start_index, len(nums)):
            self.path.append(nums[i])
            self.backtracking(nums, i+1)
            self.path.pop()

if __name__ == "__main__":
    result = Solution()
    ans = result.subsets([1,2,3])
    print(ans)