class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        preC,curC,res = 0,0,1 #题目里nums长度大于等于1，当长度为1时，其实到不了for循环
        for i in range(len(nums)-1):
            curC = nums[i+1] - nums[i]
            if curC * preC <=0 and curC !=0:
                res += 1
                preC = curC
        return res


class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        dp = []
        for i in range(len(nums)):
            # 初始为[1,1]
            dp.append([1,1])
            for j in range(i):
                # nums[i] 为波谷
                if nums[j] > nums[i]:
                    dp[i][1] = max(dp[i][1], dp[j][0]+1)
                # nums[i] 为波峰
                if nums[j] < nums[i]:
                    dp[i][0] = max(dp[i][0], dp[j][1]+1)
        return max(dp[-1][0],dp[-1][1])

