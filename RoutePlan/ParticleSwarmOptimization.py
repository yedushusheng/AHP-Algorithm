# 粒子群算法
# 最优顺序: [2 2 0 1 1]
# 最短距离: 2.336067977499784

import numpy as np

# 计算两点之间的距离
def distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

# 计算整体路径长度
def total_distance(coords, order):
    total = 0
    for i in range(len(order) - 1):
        total += distance(coords[order[i]], coords[order[i + 1]])
    return total

# 粒子群算法主函数
def particle_swarm_optimization(coords, num_particles=10, iterations=100, inertia=0.5, cognitive_param=1.0, social_param=1.0):
    num_coords = len(coords)
    # 初始化粒子的位置和速度
    particles_position = np.array([np.random.permutation(num_coords) for _ in range(num_particles)])
    particles_velocity = np.zeros((num_particles, num_coords), dtype=int)
    best_global_position = None
    best_global_distance = np.inf

    for _ in range(iterations):
        for i in range(num_particles):
            curr_distance = total_distance(coords, particles_position[i])
            if curr_distance < best_global_distance:
                best_global_distance = curr_distance
                best_global_position = particles_position[i].copy()

        for i in range(num_particles):
            for j in range(num_coords):
                # 更新速度
                rand1 = np.random.random()
                rand2 = np.random.random()
                cognitive_velocity = cognitive_param * rand1 * (particles_position[i][j] - particles_position[i][j])
                social_velocity = social_param * rand2 * (best_global_position[j] - particles_position[i][j])
                particles_velocity[i][j] = inertia * particles_velocity[i][j] + cognitive_velocity + social_velocity

            # 更新位置
            particles_position[i] += particles_velocity[i]
            particles_position[i] %= num_coords

    return best_global_position, best_global_distance

# 给定建筑的经纬度信息
buildings = [
    (32.0, 118.8),
    (32.0, 118.7),
    (31.0, 116.8),
    (32.0, 115.8),
    (32.0, 120.8)
]

# 运行粒子群算法
best_order, best_distance = particle_swarm_optimization(buildings)
print("最优顺序:", best_order)
print("最短距离:", best_distance)
