def lengthOfLongestSubstring(s):
        if not s.strip():
            return 0
        longstring=0
        total=[]
        donechar=[]
        for i in s:
            print(f'i{i}sss')
            if i not in donechar:
                longstring+=1
                donechar.append(i)
            else:
                total.append(longstring)
                longstring=0
                donechar=[i]
        total.append(longstring)
        return(max(total))
print(lengthOfLongestSubstring(' '))