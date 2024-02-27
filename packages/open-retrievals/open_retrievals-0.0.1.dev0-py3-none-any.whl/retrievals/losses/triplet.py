"""
`FaceNet: A Unified Embedding for Face Recognition and Clustering
<https://arxiv.org/abs/1503.03832>`_
"""

import torch
import torch.nn as nn


class TripletLoss(nn.Module):
    """
    https://omoindrot.github.io/triplet-loss
    """

    def __init__(self):
        pass
