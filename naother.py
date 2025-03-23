 
def find_combinations(nums, target):
    dp = [[] for i in range(target + 1)]
    dp[0] = [[]]

    for num in nums:
      for t in range(num, target + 1):
            for comb in dp[t - num]:
                dp[t].append(comb + [num])

    return dp[target]
   
print(find_combinations([int(x) for x in input().split()],int(input())))
