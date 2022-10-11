class Solution:
    def isValidBST(self, root):
        candidate_list = []
        # def __traverse(root):
        #     nonlocal candidate_list
        #     if not root:
        #         return
        #     __traverse(root.left)
        #     candidate_list.append(root.val)
        #     __traverse(root.right)

        def __traverse(root):
            nonlocal candidate_list
            if not root:
                return
            __traverse(root.left)
            candidate_list.append(root.val)
            __traverse(root.right)

        def __is_sorted(nums):
            for i in range(1, len(nums)):
                if nums[i] <= nums[i-1]:
                    return False
            return True

        __traverse(root)
        res = __is__sorted(candidate_list)