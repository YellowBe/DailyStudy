class Solution(object):
    def uniquePathsWithObstacles(self, obstacleGrid):
        n = len(obstacleGrid)
        m = len(obstacleGrid[0])
        dp = [[0] * m for _ in range(n)]
        dp[0][0] = 0 if obstacleGrid[0][0] else 1
        for i in range(1, n):
            if obstacleGrid[i][0] == 1 or dp[i-1][0] == 0:
                dp[i][0] = 0
            else:
                dp[i][0] = 1
        for j in range(1,m):
            if obstacleGrid[0][j] == 1 or dp[0][j-1]==0:
                dp[0][j] = 0
            else:
                dp[0][j] = 1
        