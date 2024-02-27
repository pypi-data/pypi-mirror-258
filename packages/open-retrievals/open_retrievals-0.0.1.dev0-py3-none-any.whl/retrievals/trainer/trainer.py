import gc
import logging
import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import accelerator
import numpy as np
import torch
import torch.nn.functional as F
import transformers
from torch import nn
from torch._tensor import Tensor
from torch.nn.modules import Module
from torch.optim.lr_scheduler import LambdaLR
from torch.optim.optimizer import Optimizer as Optimizer
from torch.utils.data import Dataset
from transformers import Trainer
from transformers.data.data_collator import DataCollator
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.trainer_callback import TrainerCallback
from transformers.trainer_utils import EvalPrediction
from transformers.training_args import TrainingArguments


@dataclass
class TrainingArguments(transformers.TrainingArguments):
    pass


class RetrievalTrainer(Trainer):
    def __init__(
        self,
        model=None,
        args: TrainingArguments = None,
        data_collator=None,
        train_dataset=None,
        eval_dataset=None,
        tokenizer=None,
        model_init=None,
        compute_metrics=None,
        callbacks=None,
        optimizers=...,
        preprocess_logits_for_metrics=None,
    ):
        super().__init__(
            model,
            args,
            data_collator,
            train_dataset,
            eval_dataset,
            tokenizer,
            model_init,
            compute_metrics,
            callbacks,
            optimizers,
            preprocess_logits_for_metrics,
        )


class RetrievalPairwiseTrainer(RetrievalTrainer):
    def __init__(
        self,
        model: Union[PreTrainedModel, Module] = None,
        args: TrainingArguments = None,
        data_collator: Optional[Any] = None,
        train_dataset: Optional[Dataset] = None,
        eval_dataset: Union[Dataset, Dict[str, Dataset], None] = None,
        tokenizer: Optional[PreTrainedTokenizerBase] = None,
        model_init: Optional[Callable[[], PreTrainedModel]] = None,
        compute_metrics: Optional[Callable[[EvalPrediction], Dict]] = None,
        callbacks: Optional[List[TrainerCallback]] = None,
        optimizers: Tuple[Optimizer, LambdaLR] = ...,
        preprocess_logits_for_metrics: Optional[Callable[[Tensor, Tensor], Tensor]] = None,
    ):
        super().__init__(
            model,
            args,
            data_collator,
            train_dataset,
            eval_dataset,
            tokenizer,
            model_init,
            compute_metrics,
            callbacks,
            optimizers,
            preprocess_logits_for_metrics,
        )

    def compute_loss(self, model, inputs, **kwargs):
        return

    def _save(self, output_dir: Optional[str] = None, state_dict=None):
        pass


class RerankerTrainer(Trainer):
    def __init__(
        self,
        model: Union[PreTrainedModel, Module] = None,
        args: TrainingArguments = None,
        data_collator: Optional[Any] = None,
        train_dataset: Optional[Dataset] = None,
        eval_dataset: Union[Dataset, Dict[str, Dataset], None] = None,
        tokenizer: Optional[PreTrainedTokenizerBase] = None,
        model_init: Optional[Callable[[], PreTrainedModel]] = None,
        compute_metrics: Optional[Callable[[EvalPrediction], Dict]] = None,
        callbacks: Optional[List[TrainerCallback]] = None,
        optimizers: Tuple[Optimizer, LambdaLR] = ...,
        preprocess_logits_for_metrics: Optional[Callable[[Tensor, Tensor], Tensor]] = None,
    ):
        super().__init__(
            model,
            args,
            data_collator,
            train_dataset,
            eval_dataset,
            tokenizer,
            model_init,
            compute_metrics,
            callbacks,
            optimizers,
            preprocess_logits_for_metrics,
        )

    def compute_loss(self, model, inputs, **kwargs):
        return

    def _save(self, output_dir: Optional[str] = None, state_dict=None):
        pass
