def two_sum(nums: list, target: int) -> tuple:
    ans = []
    d = dict()
    for i in range(len(nums)):
        if target - nums[i] in d:
            ans.append(i)
            ans.append(d[target - nums[i]])
            break
        else:
            d[nums[i]] = i
    ans.sort()
    return tuple(ans)
print(two_sum([2, 7, 11, 15]*10**5 + [5, 7], 12))