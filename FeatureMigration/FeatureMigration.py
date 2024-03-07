import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 加载预训练的 VGG19 模型
vgg = models.vgg19(pretrained=True).features

# 冻结所有参数
for param in vgg.parameters():
    param.requires_grad_(False)

# 将 VGG19 用作特征提取器
def features(image, model):
    layers = {
        '0': 'conv1_1',
        '5': 'conv2_1',
        '10': 'conv3_1',
        '19': 'conv4_1',
        '28': 'conv5_1'
    }
    x = image
    features = {}
    for name, layer in model._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x
    return features

# 加载图像
def load_image(image_path, transform=None, max_size=None, shape=None):
    image = Image.open(image_path)
    if max_size:
        scale = max_size / max(image.size)
        size = np.array(image.size) * scale
        image = image.resize(size.astype(int), Image.LANCZOS)

    if shape:
        image = image.resize(shape, Image.LANCZOS)
    if transform:
        image = transform(image).unsqueeze(0)
    return image

# 定义图像路径和超参数
content_image_path = 'D:/pycharm/PyCharm 2021.3.1/pythonProject/__building.jpg'
style_image_path = 'D:/pycharm/PyCharm 2021.3.1/pythonProject/__sky.jpg'
content_size = 256
style_size = 256

# 加载图像并进行预处理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

content = load_image(content_image_path, transform, max_size=content_size)
style = load_image(style_image_path, transform, shape=[style_size, style_size])

# 获取特征
content_features = features(content, vgg)
style_features = features(style, vgg)

# 将内容特征迁移到风格特征
target = content.clone().requires_grad_(True)
style_weights = {'conv1_1': 1.0, 'conv2_1': 0.8, 'conv3_1': 0.5, 'conv4_1': 0.3, 'conv5_1': 0.1}

content_weight = 1e4
style_weight = 1e2
learning_rate = 0.03
optimizer = torch.optim.Adam([target], lr=learning_rate)

epochs = 10000
for epoch in range(epochs):
    target_features = features(target, vgg)
    content_loss = torch.mean((target_features['conv4_1'] - content_features['conv4_1']) ** 2)
    style_loss = 0
    for layer in style_weights:
        target_feature = target_features[layer]
        target_gram = torch.mm(target_feature.view(target_feature.size(0), -1),
                               target_feature.view(target_feature.size(0), -1).t())
        style_gram = torch.mm(style_features[layer].view(style_features[layer].size(0), -1),
                              style_features[layer].view(style_features[layer].size(0), -1).t())
        layer_style_loss = style_weights[layer] * torch.mean((target_gram - style_gram) ** 2)
        style_loss += layer_style_loss

    total_loss = content_weight * content_loss + style_weight * style_loss
    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}: Total Loss: {total_loss.item()}")

# 可视化合成图像
img = target.clone().detach().numpy()
img = img.squeeze(0)
img = img.transpose(1, 2, 0)
img = img * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.456, 0.406])
img = np.clip(img, 0, 1)

plt.imshow(img)
plt.axis('off')
plt.show()
