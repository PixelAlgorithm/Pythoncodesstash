class Solution(object):
    def lengthOfLongestSubstring(self, s):
        longstring=str()
        total=[0]
        donechar=[]
        for i in s:
            if i not in donechar:
                longstring+=i
                donechar.append(i)
            else:
                total.append(len(longstring))
                longstring=i
                donechar=[i]
        total.append(len(longstring))
        return max(total)