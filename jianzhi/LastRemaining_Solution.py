# -*- coding:utf-8 -*-
class Solution:
    def LastRemaining_Solution(self, n, m):
        # write code here
        if n<=0 or m<=0:
            return -1
        last =0
        for i in range(1,n+1):
            last = (last+m)%i
        return last
s=Solution()
print s.LastRemaining_Solution(5,2)