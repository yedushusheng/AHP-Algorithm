# 模拟退火算法
# 最优路径顺序: [4, 0, 1, 2, 3]
# 最短距离: 555.8364186993853

import math
import random

########################################################################
####  建筑遗产更新过程中如何规划不同建筑之间的路径，以节省耗材又实现空间最大利用   ####
########################################################################

# 建筑物的经纬度信息
buildings = [
    (32.00468281747915, 118.79161465269148),
    (32.00423820243287, 118.7916449593948),
    (32.00400432891307, 118.79165405140583),
    (32.004749638051166, 118.79107519337208),
    (32.00459286663223, 118.79105700935007),
    (32.00437955427097, 118.79099336527305),
    (32.00424334250356, 118.79095699722903),
    (32.00429988326176, 118.79127521761407),
    (32.00406857993949, 118.79112065342707),
    (32.00394521792898, 118.79091153717404),
    (32.00383213594019, 118.79107519337208),
    (32.004233062364484, 118.78985080254108),
    (32.00382185575504, 118.78964774762872),
    (32.00385269631472, 118.7900417347721),
    (32.004551746218205, 118.78945681539768),
    (32.00409428033999, 118.78942953936466),
    (32.00438983439867, 118.788405172774),
    (32.005147990464565, 118.78690499093243),
    (32.004384694347706, 118.78727473271316)
]

# 计算两个经纬度坐标之间的距离（可以使用球面三角形距离公式）
def distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # 地球平均半径，单位：千米

    # 将角度转换为弧度
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # 计算经纬度之间的差值
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # 使用球面三角形距离公式计算两点之间的距离
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

# 计算总距离
def total_distance(order):
    total = 0
    for i in range(len(order) - 1):
        total += distance(buildings[order[i]], buildings[order[i + 1]])
    return total

# 模拟退火算法
def simulated_annealing(buildings, iterations=10000, temp=1000, cooling_rate=0.003):
    current_order = list(range(len(buildings)))
    random.shuffle(current_order)
    current_distance = total_distance(current_order)

    for i in range(iterations):
        # 生成新的解
        new_order = current_order[:]
        index1 = random.randint(0, len(buildings) - 1)
        index2 = random.randint(0, len(buildings) - 1)
        new_order[index1], new_order[index2] = new_order[index2], new_order[index1]
        new_distance = total_distance(new_order)

        # 计算能量变化
        delta_distance = new_distance - current_distance

        # 根据能量变化和温度决定是否接受新解
        if delta_distance < 0 or random.random() < math.exp(-delta_distance / temp):
            current_order = new_order
            current_distance = new_distance

        # 降低温度
        temp *= 1 - cooling_rate

    return current_order, current_distance

# 运行模拟退火算法
best_order, min_distance = simulated_annealing(buildings)

print("最优路径顺序:", best_order)
print("最短距离:", min_distance)

