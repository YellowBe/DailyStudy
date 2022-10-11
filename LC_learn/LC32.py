class Solution:
    def longestValidParentheses(self, s):
        max_length = 0
        stck = [-1] # initialize with a start index
        for i in range(len(s)):
            if s[i] == '(':
                stck.append(i)
            else:
                stck.pop()
                if not stck: # if popped -1, add a new start index
                    stck.append(i)
                else:
                    max_length = max(max_length, i-stck[-1])
        return max_length


if __name__ == "__main__":
    result = Solution()
    ans = result.longestValidParentheses("(()()")
    print(ans)