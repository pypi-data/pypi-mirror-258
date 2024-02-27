[license-image]: https://img.shields.io/badge/License-Apache%202.0-blue.svg
[license-url]: https://opensource.org/licenses/Apache-2.0
[pypi-image]: https://badge.fury.io/py/retrievals.svg
[pypi-url]: https://pypi.python.org/pypi/retrievals
[pepy-image]: https://pepy.tech/badge/retrievals/month
[pepy-url]: https://pepy.tech/project/retrievals
[build-image]: https://github.com/LongxingTan/Retrievals/actions/workflows/test.yml/badge.svg?branch=master
[build-url]: https://github.com/LongxingTan/Retrievals/actions/workflows/test.yml?query=branch%3Amaster
[lint-image]: https://github.com/LongxingTan/Retrievals/actions/workflows/lint.yml/badge.svg?branch=master
[lint-url]: https://github.com/LongxingTan/Retrievals/actions/workflows/lint.yml?query=branch%3Amaster
[docs-image]: https://readthedocs.org/projects/Retrievals/badge/?version=latest
[docs-url]: https://retrievals.readthedocs.io/en/latest/?version=latest
[coverage-image]: https://codecov.io/gh/longxingtan/Retrievals/branch/master/graph/badge.svg
[coverage-url]: https://codecov.io/github/longxingtan/Retrievals?branch=master
[contributing-image]: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
[contributing-url]: https://github.com/longxingtan/Retrievals/blob/master/CONTRIBUTING.md
[codeql-image]: https://github.com/longxingtan/Retrievals/actions/workflows/codeql-analysis.yml/badge.svg
[codeql-url]: https://github.com/longxingtan/Retrievals/actions/workflows/codeql-analysis.yml

<h1 align="center">
<img src="./docs/source/_static/logo.svg" width="490" align=center/>
</h1><br>

[![LICENSE][license-image]][license-url]
[![PyPI Version][pypi-image]][pypi-url]
[![Download][pepy-image]][pepy-url]
[![Build Status][build-image]][build-url]


**[Documentation](https://retrievals.readthedocs.io)** | **[Tutorials](https://retrievals.readthedocs.io/en/latest/tutorials.html)** | **[Release Notes](https://retrievals.readthedocs.io/en/latest/CHANGELOG.html)** | **[中文](https://github.com/LongxingTan/retrievals/blob/master/README_zh-CN.md)**

**Retrievals** is an easy-to-use python framework supporting state-of-the-art embeddings, especially for retrieval and rerank in NLP/LLM, based on PyTorch and Transformers.


## Usage

**Pretrained weight embedding**
```python

```


**Contrastive finetune transformers model**
```python
from retrievals import AutoModelForEmbedding, AutoModelForMatch
from retrievals.losses import ArcFaceAdaptiveMarginLoss
from retrievals.trainer import CustomTrainer, train_fn


train_dataset = RetrievalTrainDataset(topic_df, tokenizer, CFG.max_len, aug=False)

train_loader = DataLoader(
    train_dataset,
    batch_size=CFG.batch_size,
    shuffle=True,
    num_workers=CFG.num_workers,
    pin_memory=False,
    drop_last=True,
)

loss_fn = ArcFaceAdaptiveMarginLoss(
    criterion=cross_entropy,
    in_features=768,
    out_features=CFG.num_classes,
    scale=CFG.arcface_scale,
    margin=CFG.arcface_margin,
)
model = AutoModelForEmbedding(CFG.MODEL_NAME, pooling_method="cls", loss_fn=loss_fn)

optimizer = get_optimizer(model, lr=CFG.learning_rate)
scheduler = get_scheduler(
    optimizer=optimizer, cfg=CFG, total_steps=len(train_dataset)
)
trainer = CustomTrainer(model, device="cuda", apex=CFG.apex)
trainer.train(
    train_loader=train_loader,
    criterion=None,
    optimizer=optimizer,
    epochs=CFG.epochs,
    scheduler=scheduler,
    dynamic_margin=True,
)
torch.save(model.state_dict(), CFG.output_dir + f"model_{CFG.exp_id}.pth")
```

**Contrastive finetune for LLM**
```python

model = AutoModelForEmbedding('llama', pooling_method='last', query_instruction='')
```


**KNN search**
```python
retrieval_model = TextRetrievals(vec_model)
retrieval_model.query('knn')

```

**Faiss search**
```python

```

**Integrated with sentence-transformer**
```python

```



**Rerank**
```python

```


## Acknowledge and Reference
