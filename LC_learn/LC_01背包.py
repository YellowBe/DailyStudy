def test_2_wei_bag_problem1(bag_size, weight, value):
    rows, cols = len(weight), bag_size + 1
    dp = [[0 for _ in range(cols)] for _ in range(rows)]

    # 初始化dp数组
    for i in range(rows):
        dp[i][0] = 0
    first_item_weight, first_item_value = weight[0], value[0]
    for j in range(1, cols):
        if first_item_weight<=j:
            dp[0][j] = first_item_value
    
    # 更新dp数组： 先遍历物品， 再遍历背包
    for i in range(1, len(weight)):
        cur_weight, cur_val = weight[i], value[i]
        for j in range(1,cols):
            if cur_weight > j: #说明背包装不下当前物品
                dp[i][j] = dp[i-1][j] 
            else:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-cur_weight] + cur_val)

