class Solution:
    def removeElement(self, nums, val: int) -> int:
        if nums is None or len(nums)==0: 
            return 0 
        l=0
        r=len(nums)-1
        while l<r: 
            while(l<r and nums[l]!=val):
                l+=1
            while(l<r and nums[r]==val):
                r-=1
            nums[l], nums[r]=nums[r], nums[l]
        print(nums)
        if nums[l]==val: 
            return l 
        else: 
            return l+1

if __name__ == "__main__":
    result = Solution()
    ans = result.removeElement(nums = [0,1,2,2,3,0,4,2], val = 2)
    print(ans)