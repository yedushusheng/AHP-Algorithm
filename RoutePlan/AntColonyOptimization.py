# 蚁群算法
# 最优顺序: [4 0 1 2 3]
# 最短距离: 5.661304617731483

import numpy as np


# 计算两点之间的距离
def distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return np.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)


# 计算整体路径长度
def total_distance(coords, order):
    total = 0
    for i in range(len(order) - 1):
        total += distance(coords[order[i]], coords[order[i + 1]])
    return total


# 初始化蚂蚁的路径
def initialize_ant(coords):
    return np.random.permutation(len(coords))


# 更新信息素
def update_pheromone(trails, ants, coords, evaporation_rate=0.5):
    trails *= evaporation_rate
    for ant in ants:
        for i in range(len(ant) - 1):
            trails[ant[i], ant[i + 1]] += 1.0 / total_distance(coords, ant)
    return trails


# 蚁群算法主函数
def ant_colony_optimization(coords, num_ants=10, iterations=100):
    num_coords = len(coords)
    trails = np.ones((num_coords, num_coords))  # 初始化信息素
    best_order = None
    best_distance = np.inf

    for _ in range(iterations):
        ants = [initialize_ant(coords) for _ in range(num_ants)]
        for ant in ants:
            curr_distance = total_distance(coords, ant)
            if curr_distance < best_distance:
                best_distance = curr_distance
                best_order = ant

        trails = update_pheromone(trails, ants, coords)

    return best_order, best_distance


# 给定建筑的经纬度信息
buildings = [
    (32.0, 118.8),
    (32.0, 118.7),
    (31.0, 116.8),
    (32.0, 115.8),
    (32.0, 120.8)
]

# 运行蚁群算法
best_order, best_distance = ant_colony_optimization(buildings)
print("最优顺序:", best_order)
print("最短距离:", best_distance)
