# 遗传算法
# 最优路径顺序: [4, 0, 1, 2, 3]
# 最短距离: 555.8364186993853

import math
import random

# 建筑物的经纬度信息
buildings = [
    (32.0, 118.8),
    (32.0, 118.7),
    (31.0, 116.8),
    (32.0, 115.8),
    (32.0, 120.8)
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

# 初始化种群
def initial_population(pop_size, num_buildings):
    population = []
    for _ in range(pop_size):
        individual = list(range(num_buildings))
        random.shuffle(individual)
        population.append(individual)
    return population

# 选择
def selection(population, num_selected, fitness):
    selected = []
    for _ in range(num_selected):
        idx = random.choices(range(len(population)), weights=fitness)[0]
        selected.append(population[idx])
    return selected

# 交叉
def crossover(parent1, parent2):
    child = [None] * len(parent1)
    start = random.randint(0, len(parent1) - 1)
    end = random.randint(0, len(parent1) - 1)
    if start > end:
        start, end = end, start

    for i in range(start, end + 1):
        child[i] = parent1[i]

    for i, gene in enumerate(parent2):
        if gene not in child:
            for j in range(len(child)):
                if child[j] is None:
                    child[j] = gene
                    break

    return child

# 变异
def mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# 遗传算法
def genetic_algorithm(buildings, pop_size=100, num_generations=1000, mutation_rate=0.1):
    num_buildings = len(buildings)
    population = initial_population(pop_size, num_buildings)
    best_distance = float('inf')
    best_order = None

    for gen in range(num_generations):
        # 计算每个个体的适应度
        fitness = [1 / (total_distance(individual) + 1) for individual in population]

        # 选择
        selected = selection(population, pop_size // 2, fitness)

        # 交叉和变异
        children = []
        for i in range(0, len(selected), 2):
            child1 = crossover(selected[i], selected[i + 1])
            child1 = mutation(child1, mutation_rate)
            child2 = crossover(selected[i + 1], selected[i])
            child2 = mutation(child2, mutation_rate)
            children.extend([child1, child2])

        # 形成新一代种群
        population = children

        # 更新最佳个体
        for individual in population:
            dist = total_distance(individual)
            if dist < best_distance:
                best_distance = dist
                best_order = individual

    return best_order, best_distance

# 运行遗传算法
best_order, min_distance = genetic_algorithm(buildings)

print("最优路径顺序:", best_order)
print("最短距离:", min_distance)
