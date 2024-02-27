import datasets
from torch.utils.data import Dataset
from transformers import DataCollatorWithPadding, PreTrainedTokenizer


class RetrievalDataset(Dataset):
    def __init__(self):
        super().__init__()

    def __len__(self):
        return

    def __getitem__(self, item):
        return
