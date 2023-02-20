#单调栈时间复杂度为O(n)
# 单调栈递增（！！！从栈口到栈底顺序），就是求右边第一个比自己大的，反之递减就是求右边第一个比自己小的。
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = [0] * len(temperatures)
        stack = [0]
        for i in range(1, len(temperatures)):
            if temperatures[i]<=temperatures[stack[-1]]:
                stack.append(i)
            else:
                while len(stack) != 0 and temperatures[i]>temperatures[stack[-1]]:
                    answer[stack[-1]] = i - stack[-1]
                    stack.pop()
                stack.append(i)
        
        return answer

# 下一个更大元素
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = [-1]*len(nums1)
        stack = [0]
        for i in range(1,len(nums2)):
            if nums2[i]<=nums2[stack[-1]]:
                stack.append(i)
            else:
                while len(stack)!=0 and nums2[i]>nums2[stack[-1]]:
                    if nums2[stack[-1]] in nums1:
                        index = nums1.index(nums2[stack[-1]])
                        result[index]=nums2[i]
                    stack.pop()
                stack.append(i)
        return result

class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        dp = [-1] * len(nums)
        stack = []
        for i in range(len(nums)*2):
            while(len(stack) != 0 and nums[i%len(nums)] > nums[stack[-1]]):
                dp[stack[-1]] = nums[i%len(nums)]
                stack.pop()
            stack.append(i%len(nums))
        return dp

# 接雨水
class Solution:
    def trap(self, height: List[int]) -> int:
        '''
        单调栈是按照 行 的方向来计算雨水
        从栈顶到栈底的顺序：从小到大
        通过三个元素来接水：栈顶，栈顶的下一个元素，以及即将入栈的元素
        雨水高度是 min(凹槽左边高度, 凹槽右边高度) - 凹槽底部高度
        雨水的宽度是 凹槽右边的下标 - 凹槽左边的下标 - 1（因为只求中间宽度）
        '''
        # stack储存index，用于计算对应的柱子高度
        stack = [0]
        result = 0
        for i in range(1, len(height)):
            #情况一
            if height[i] < height[stack[-1]]:
                stack.append(i)
            # 情况二
            # 当当前柱子高度和栈顶一致时，左边的一个是不可能存放雨水的，所以保留右侧新柱子
            # 需要使用最右边的柱子来计算宽度
            elif height[i] == height[stack[-1]]:
                stack.pop()
                stack.append(i)
            # 情况三
            else:
                # 抛出所有较低的柱子
                #反正中间都是不参与计算宽度的，只需要他的高度，所以不用担心高度相等被抛掉的情况
                while stack and height[i] > height[stack[-1]]:
                    # 栈顶就是中间的柱子: 储水槽，就是凹槽的底部
                    mid_height = height[stack[-1]]
                    stack.pop()
                    if stack:
                        right_height = height[i]
                        left_height = height[stack[-1]]
                        # 两侧的较矮一方的高度 - 凹槽底部高度
                        h = min(right_height, left_height) - mid_height
                        # 凹槽右侧下标 - 凹槽左侧下标 - 1: 只求中间宽度
                        w = i - stack[-1] - 1
                        result += h * w
                stack.append(i)
        return result