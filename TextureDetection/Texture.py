import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
image = cv2.imread('D:/pycharm/PyCharm 2021.3.1/pythonProject/__building.jpg')  # 替换成您的图像路径
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用Gabor滤波器提取纹理特征
ksize = 31  # Gabor滤波器尺寸
sigma = 4.0  # Gabor滤波器标准差
theta = np.pi / 4  # Gabor滤波器方向
lambda_ = 10.0  # Gabor滤波器波长
gamma = 0.5  # Gabor滤波器纵横比

gabor_kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambda_, gamma, 0, ktype=cv2.CV_32F)
image_filtered = cv2.filter2D(image_gray, cv2.CV_32F, gabor_kernel)

# 生成纹理图像的频谱图
f = np.fft.fft2(image_filtered)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20 * np.log(np.abs(fshift))

# 显示原始图像、滤波后的图像和频谱图
plt.figure(figsize=(12, 6))

plt.subplot(131), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original Image'), plt.axis('off')

plt.subplot(132), plt.imshow(image_filtered, cmap='gray')
plt.title('Filtered Image'), plt.axis('off')

plt.subplot(133), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.axis('off')

plt.tight_layout()
plt.show()
