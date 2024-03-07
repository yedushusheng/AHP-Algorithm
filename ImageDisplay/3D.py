import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image

# 读取图像
image_path = 'D:/pycharm/PyCharm 2021.3.1/pythonProject/__building.jpg'
image = Image.open(image_path)
image = np.array(image)

# 创建三维图像空间
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 图像的尺寸
height, width, _ = image.shape

# 生成立体图像的数据
x, y = np.linspace(0, width - 1, width), np.linspace(0, height - 1, height)
x, y = np.meshgrid(x, y)
z = np.zeros_like(x)

# 绘制立体图像
ax.plot_surface(x, y, z, facecolors=image/255.0, rstride=1, cstride=1, shade=False)

# 隐藏坐标轴
ax.axis('off')

# 显示图像
plt.show()
