"""
`SimCSE: Simple Contrastive Learning of Sentence Embeddings
<https://arxiv.org/abs/2104.08821>`_
"""

import torch
import torch.nn.functional as F
from torch import nn


class SimCSE(nn.Module):
    def __init__(self, criterion, temperature=0.05, device="cuda"):
        super().__init__()
        # TODO: dynamic_temperature
        self.criterion = criterion
        self.temperature = temperature
        self.device = device

    def forward(self, query_embeddings, content_embeddings, negative_embeddings=None):
        y_true = torch.arange(0, query_embeddings.size(0), device=self.device)

        sim = F.cosine_similarity(
            query_embeddings.unsqueeze(1), content_embeddings.unsqueeze(0), dim=2
        )
        # sim = sim - torch.eye(y_pred.shape[0], device=device) * 1e12

        sim = sim / self.temperature
        loss = self.criterion(sim, y_true)
        loss = torch.mean(loss)
        return loss
