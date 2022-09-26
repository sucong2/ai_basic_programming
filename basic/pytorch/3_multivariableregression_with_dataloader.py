# -*- coding: utf-8 -*-
"""3_MultiVariableRegression_with_DataLoader.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h2691y8-os3CRRSS9ZEZJPZF8Gj1aQ0-

### 다중 선형 회귀
y_pred = w1*x1+w2*x2+w3*x3+b
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import TensorDataset, DataLoader

"""### 1. 다중 선형 회귀를 위한 데이터 & 데이터로더 생성"""

x_train  =  torch.FloatTensor([[73,  80,  75], 
                               [93,  88,  93], 
                               [89,  91,  90], 
                               [96,  98,  100],   
                               [73,  66,  70]])  
y_train  =  torch.FloatTensor([[152],  [185],  [180],  [196],  [142]])

# 데이터셋에 넣어서 데이터 로더 사용
dataset = TensorDataset(x_train, y_train)

# 데이터 로더를 통해서 원하는 형태로 데이터를 공급 받는다.
BATCH_SIZE = 2

# DataLoader는 잘 섞어서 batch_size만큼씩 끊어서 데이터를 공급해준다.
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

"""![스크린샷 2022-09-16 오후 10.01.52.png](data:image/png;base64,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)

### 2. 모델 선언
"""

model = nn.Linear(3,1)

LR = 1e-5  # 10의 마이너스 5승
optimizer = torch.optim.SGD(model.parameters(), lr=LR)

epochs = 40
for epoch in range(epochs+1):
    # 전체 훈련 데이터는 5개인데 batch_size=2이므로 2,2,1개 -> 1 epoch
    for batch_idx, samples in enumerate(dataloader):
        x_train, y_train = samples
        y_pred = model(x_train)

        Loss = F.mse_loss(y_pred, y_train)

        optimizer.zero_grad()
        Loss.backward()
        optimizer.step()

        if epoch%5==0:
            print('Epoch {:4d}/{} Batch {}/{} Loss: {:.6f}'.format(
            epoch, epochs, batch_idx+1, len(dataloader),
            Loss.item()))
