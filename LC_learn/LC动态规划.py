# 递增子序列
def lengthOfLIS(self, nums):
    if len(nums) <= 1:
        return len(nums)
    dp = [1] * len(nums)
    result = 0
    for i in range(1, len(nums)):
        for j in range(0, i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
        result = max(result, dp[i])
    return result

# 最长连续递增子序列
def findLengthOfLCIS(self, nums: List[int]) -> int:
    if len(nums) == 0:
        return 0
    result = 1
    dp = [1] * len(nums)
    for i in range(len(nums)-1):
        if nums[i+1] > nums[i]:
            dp[i+1] = dp[i] + 1
        result = max(result, dp[i+1])
    return result

#最长公共子序列 等同于 不相交的线
class Solution:
    def longestCommonSubsequence(self, text1, text2):
        len1, len2 = len(text1) + 1, len(text2)+1
        dp = [[0 for _ in range(len1)] for _ in range(len2)]
        for i in range(1, len2):
            for j in range(1,len1):
                if text1[j-1] == text2[i-1]:
                    dp[i][j] = dp[i-1][j-1]+1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[-1][-1]