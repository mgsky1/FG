'''
@desc: 使用存储的中间模型，随机生成300张图片
@author: Martin Huang
@time: created on 2020/7/18 23:24
@修改记录:
'''
import torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from torchvision.utils import save_image
import random
import os.path

channels = 3
img_size = 256
latent_dim = 100
# cuda = True if torch.cuda.is_available() else False
cuda = False
Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()

        self.init_size = img_size // 4
        self.l1 = nn.Sequential(nn.Linear(latent_dim, 128 * self.init_size ** 2))

        self.conv_blocks = nn.Sequential(
            nn.BatchNorm2d(128),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 128, 3, stride=1, padding=1),
            nn.BatchNorm2d(128, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 64, 3, stride=1, padding=1),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, channels, 3, stride=1, padding=1),
            nn.Tanh(),
        )

    def forward(self, z):
        out = self.l1(z)
        out = out.view(out.shape[0], 128, self.init_size, self.init_size)
        img = self.conv_blocks(out)
        return img


if __name__ == '__main__':
    for i in range(300):
        k = random.randint(1,9)
        model = torch.load(os.path.join('model','gen-'+str(k)+'.pth'),map_location=lambda storage, loc: storage)
        z = Variable(Tensor(np.random.normal(0, 1, (1, latent_dim))))
        fake = model(z)
        save_image(fake,os.path.join('select',str(i)+'.png'),normalize=True)
        print('%d pic(s) has generated'%(i))
