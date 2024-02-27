"""
`Representation Learning with Contrastive Predictive Coding
<https://arxiv.org/abs/1807.03748v2>`_
"""

from typing import Callable, Union

import torch
import torch.distributed.nn
import torch.nn as nn
import torch.nn.functional as F


class InfoNCE(nn.Module):
    def __init__(
        self,
        criterion: Union[nn.Module, Callable, None] = None,
        device="cuda" if torch.cuda.is_available() else "cpu",
    ):
        super().__init__()
        self.criterion = criterion
        self.device = device

    def forward(
        self,
        query_embeddings,
        positive_embeddings,
        negative_embeddings=None,
        negative_mode='paired',
        logit_scale=1,
    ):
        query_embeddings = F.normalize(query_embeddings, dim=-1)
        positive_embeddings = F.normalize(positive_embeddings, dim=-1)
        if negative_embeddings is None:
            logits1 = logit_scale * query_embeddings @ positive_embeddings.T
            logits2 = logits1.T
            labels = torch.arange(len(logits1), dtype=torch.long, device=self.device)
            loss = (self.criterion(logits1, labels) + self.criterion(logits2, labels)) / 2
            return loss
        else:
            negative_embeddings = F.normalize(negative_embeddings, dim=-1)
            positive_logit = torch.sum(query_embeddings * positive_embeddings, dim=1, keepdim=True)

            if negative_mode == 'unpaired':
                # Cosine between all query-negative combinations
                negative_logits = query_embeddings @ negative_embeddings.transpose(-2, -1)

            elif negative_mode == 'paired':
                query = query_embeddings.unsqueeze(1)
                negative_logits = query @ negative_embeddings.transpose(-2, -1)
                negative_logits = negative_logits.squeeze(1)

            # First index in last dimension are the positive samples
            logits = torch.cat([positive_logit, negative_logits], dim=1)
            labels = torch.zeros(len(logits), dtype=torch.long, device=query_embeddings.device)
            return self.criterion(logits, labels)
