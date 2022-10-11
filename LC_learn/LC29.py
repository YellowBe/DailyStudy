class Solution:
    def divide(self, dividend: int, divisor: int) -> int:

        def div(a: int, b: int) -> int:
            if (a < b):
                return 0

            count = 1
            mb = b
            while (mb + mb <= a):
                count <<= 1 # count * 2
                mb <<= 1 # mb * 2
            
            return count + div(a - mb, b)

        INT_MIN, INT_MAX = -2**31, 2**31 - 1
        divid = abs(dividend)
        divis = abs(divisor)
        res = div(divid, divis)
        res = -res if (dividend * divisor < 0) else res
        if (res > INT_MAX or res < INT_MIN):
            return INT_MAX
        
        return res

if __name__ == "__main__":
    result = Solution()
    ans = result.divide(10,3)
    print(ans)