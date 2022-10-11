class Solution:
    # 思路1：优先考虑胃饼干
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()
        s.sort()
        start, count = len(s) - 1, 0
        for index in range(len(g) - 1, -1, -1):
            if start >= 0 and g[index] <= s[start]:
                start -= 1
                count += 1
        return count
