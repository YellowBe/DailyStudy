class Solution:
    def reconstructQueue(self, people):
        people.sort(key=lambda x: (x[0], -x[1]))
        n = len(people)
        ans = [[] for _ in range(n)]
        for person in people:
            spaces = person[1] + 1
            for i in range(n):
                if not ans[i]:
                    spaces -= 1
                    if spaces == 0:
                        ans[i] = person
                        break
        return ans
if __name__ == "__main__":
    result = Solution()
    ans = result.reconstructQueue([[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]])
    print(ans)