"""
trainable temperature parameter: Text and Code Embeddings by Contrastive Pre-Training
"""

import torch
import torch.nn.functional as F
from torch import nn


class CosineSimilarity(nn.Module):
    def __init__(self, temperature):
        self.temperature = temperature

    def forward(self, query_embeddings, content_embeddings):
        sim_pos_vector = torch.cosine_similarity(query_embeddings, content_embeddings, dim=-1)
        sim_pos_vector = sim_pos_vector / self.temperature
        sim_neg_matrix = torch.cosine_similarity(
            query_embeddings.unsqueeze(1),
            content_embeddings.unsqueeze(0),
            dim=-1,
        )
        sim_neg_matrix = sim_neg_matrix / self.temperature
        sim_diff_matrix = sim_pos_vector.unsqueeze(1) - sim_neg_matrix
        loss = -torch.log(torch.sigmoid(sim_diff_matrix)).mean()
        return loss

    def get_temperature(self):
        if not self.dynamic_temperature:
            return self.temperature
        return torch.clamp(self.temperature, min=1e-3)


class TripletCosineSimilarity(nn.Moduel):
    def __init__(self, temperature: float = 0, margin: float = 0.50):
        super().__init__()
        self.temperature = temperature
        self.margin = margin
        self.distance_metric = lambda x, y: F.pairwise_distance(x, y, p=2)

    def forward(self, query_embedding, content_pos_embedding, content_neg_embedding):
        distance_pos = self.distance_metric(query_embedding, content_pos_embedding)
        distance_neg = self.distance_metric(query_embedding, content_neg_embedding)

        losses = F.relu(distance_pos - distance_neg + self.margin)
        return losses.mean()


class Similarity(nn.Module):
    """
    Dot product or cosine similarity
    """

    def __init__(self, temp=0.05):
        super().__init__()
        self.temp = temp
        self.cos = nn.CosineSimilarity(dim=-1)

    def forward(self, x, y):
        return self.cos(x, y) / self.temp
