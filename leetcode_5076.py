#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/6/2 0002 上午 10:35
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
import time
import re

__author__ = 'Max_Pengjb'
start_time = time.time()


# 下面写上代码块

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        i, j = len(str1), len(str2)
        if i > j:
            str1, str2 = str2, str1
        if not re.match(str1, str2):
            return ""
        cc = self.mc(i, j)
        ccs = self.allc(cc)[::-1]
        print(i, j)
        print(ccs)
        for x in ccs:
            if self.isnot(x, str2):
                return str1[0:x:]
        return ""

    # 辗转相除法：辗转相除法是求两个自然数的最大公约数的一种方法，也叫欧几里德算法。
    # 假设 a < b,分析一下，其实 a b 哪个位置无所谓
    # mc(a,b) = mc(b%a,a) if b%a != 0 else a
    def mc(self, a, b) -> int:
        return self.mc(b % a, a) if b % a != 0 else a

    def allc(self, k) -> list:
        r = []
        for i in range(1, k + 1):
            if k % i == 0:
                r.append(i)
        return r

    def isnot(self, n, stri):
        patt = stri[0:n:]
        for j in range(0, len(stri), n):
            print(n, patt, stri[j:j + n:])
            if patt != stri[j:j + n:]:
                return False
        return True


mmcc = Solution().gcdOfStrings("ABCABC", "ABC")
print("ss  :" + mmcc)
# 上面中间写上代码块
end_time = time.time()
print('Running time: %s Seconds' % (end_time - start_time))
