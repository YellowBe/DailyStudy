class Solution:
    def reverseWords(self, s: str) -> str:
        w = s.split(' ')
        ans = []
        for i in w:
            ans.append(i[::-1])
        result = ' '.join(ans)
        return result
    
    def reverseWords(self, s: str) -> str:
        w = s.split(' ')
        ans = []
        for i in w:
            ans.append(i[::-1])
        result = ' '.join(ans)
        return result 

    def reverseWords(self, s: str) -> str:
        w = s.split(' ')
        ans = []
        for i in w:
            ans.append(i[::-1])
        result = ' '.join(ans)
        return result
        # revstr = ''
        # flag = 0
        # for i in ans:
        #     if flag == 1:
        #         revstr = revstr + ' ' + i 
        #     else:
        #         revstr = i 
        #     flag = 1
        # return revstr

if __name__ == "__main__":
    result = Solution()
    ans = result.reverseWords("Let's take LeetCode contest")
    print(ans)