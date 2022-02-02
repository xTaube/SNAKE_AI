import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from .model import Linear_QNet


class QTrainer:
    def __init__(self, model: Linear_QNet, lr: float, gamma: float):
        self.lr = lr
        self.gama = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameter(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state: np.array, action: list, reward: int, next_state: np.array, done: bool) -> None:
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma*torch.max*self.model(next_state[idx])

            target[idx][torch.argmax(action).item()] = Q_new
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()