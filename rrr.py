def find_combinations(nums, target):
    dp = [[] for i in range(target + 1)]
    dp[0] = [[]]

    for num in nums:
        print('num',num)
        for t in range(num, target + 1):
            print('t',t)
            for comb in dp[t - num]:
                print('comb',comb)
                dp[t].append(comb + [num])

    return dp[target]
   

print(find_combinations([int(x) for x in input().split()],int(input())))
