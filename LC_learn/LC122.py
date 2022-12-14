class Solution:
    def maxProfit(self,prices):
        result = 0
        for i in range(1, len(prices)):
            result += max(prices[i] - prices[i-1], 0)
        return result
        