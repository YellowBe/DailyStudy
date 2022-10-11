class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        count = 2 ** k
        str_set = set()
        for i in range(0,len(s)-k+1):
            str_set.add(s[i:i+k])
        print(str_set)
        return 1
if __name__ == "__main__":
    result = Solution()
    ans = result.hasAllCodes("00110",2)
    print(ans)