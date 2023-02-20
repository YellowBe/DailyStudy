class Solution:
    def removeElement(self, nums) -> int:
        n = len(nums)
        left = right = 0
        while right < n:
            if nums[right] != 0:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
            right += 1
if __name__ == "__main__":
    result = Solution()
    ans = result.removeElement([4,12,0,0,1,1,2])
    print(ans)