import torch
import torch.nn as nn
import torch.nn.functional as F


class Generator(nn.Module):
    def __init__(self, ht_dim, ecg_dim):
        super(Generator, self).__init__()

        def block(in_feat, out_feat, normalize=True):
            layers = [nn.Linear(in_feat, out_feat)]
            if normalize:
                layers.append(nn.BatchNorm1d(out_feat, 0.8))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            return layers

        self.model = nn.Sequential(
            *block(ht_dim, 128, normalize=False),
            *block(128, 256),
            *block(256, 512),
            *block(512, 1024),
            nn.Linear(1024, ecg_dim),
            nn.Tanh()
        )

    def forward(self, noise, ht):
        gen_input = torch.cat((noise, ht), -1)
        ecg = self.model(ht)
        return ecg


class Discriminator(nn.Module):
    def __init__(self, ecg_dim):
        super(Discriminator, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(ecg_dim, 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
        )

    def forward(self, ecg):
        validity = self.model(ecg)
        return validity