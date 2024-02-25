r"""Contain the implementation of a ``IterDataPipe`` to generate mini-
batches."""

from __future__ import annotations

__all__ = ["MiniBatcherIterDataPipe"]

import logging
from typing import TYPE_CHECKING, TypeVar

from coola.utils.format import str_indent
from torch.utils.data import IterDataPipe
from torch.utils.data.datapipes.iter import IterableWrapper

from redcat.base import BaseBatch
from redcat.utils.tensor import get_torch_generator

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)

T = TypeVar("T")


class MiniBatcherIterDataPipe(IterDataPipe[BaseBatch[T]]):
    r"""Implement a DataPipe to generate mini-batches from a batch
    (``BaseBatch`` object).

    Args:
        datapipe_or_batch: Specifies the datapipe of batches to split.
            The generated mini-batches have the same structure
            as the input batches.
        batch_size: Specifies the batch size.
        drop_last: If ``True``, it drops the last incomplete batch,
            if the number of examples is not divisible by the
            batch size. If ``False`` and the number of examples is
            not divisible by the batch size, then the
            last batch will be smaller.
        shuffle: If ``True``, the batches are shuffled before to
            create the mini-batches. The shuffling is done per batch.
        random_seed: Specifies the random seed used to shuffle the
            batch before to split it.

    Example usage:

    ```pycon
    >>> import torch
    >>> from torch.utils.data.datapipes.iter import IterableWrapper
    >>> from redcat import BatchedTensor
    >>> from redcat.datapipes.iter import MiniBatcher
    >>> datapipe = MiniBatcher(
    ...     IterableWrapper([BatchedTensor(torch.arange(4).add(i * 4)) for i in range(2)]),
    ...     batch_size=2,
    ... )
    >>> list(datapipe)
    [tensor([0, 1], batch_dim=0),
     tensor([2, 3], batch_dim=0),
     tensor([4, 5], batch_dim=0),
     tensor([6, 7], batch_dim=0)]
    >>> datapipe = MiniBatcher(BatchedTensor(torch.arange(9)), batch_size=2)
    >>> list(datapipe)
    [tensor([0, 1], batch_dim=0),
     tensor([2, 3], batch_dim=0),
     tensor([4, 5], batch_dim=0),
     tensor([6, 7], batch_dim=0),
     tensor([8], batch_dim=0)]

    ```
    """

    def __init__(
        self,
        datapipe_or_batch: IterDataPipe[BaseBatch[T]] | BaseBatch[T],
        batch_size: int,
        drop_last: bool = False,
        shuffle: bool = False,
        random_seed: int = 5513175564631803238,
    ) -> None:
        self._datapipe_or_batch = datapipe_or_batch
        self._batch_size = int(batch_size)
        self._drop_last = bool(drop_last)
        self._shuffle = bool(shuffle)
        self._generator = get_torch_generator(random_seed)

    def __iter__(self) -> Iterator[BaseBatch[T]]:
        logger.info("Starting to create mini-batches...")
        datapipe_or_batch = self._datapipe_or_batch
        if isinstance(datapipe_or_batch, BaseBatch):
            datapipe_or_batch = IterableWrapper([datapipe_or_batch])
        for item in datapipe_or_batch:
            batch = item.shuffle_along_batch(self._generator) if self._shuffle else item
            yield from batch.to_minibatches(batch_size=self._batch_size, drop_last=self._drop_last)

    def __len__(self) -> int:
        if isinstance(self._datapipe_or_batch, BaseBatch):
            return self._datapipe_or_batch.get_num_minibatches(
                batch_size=self._batch_size, drop_last=self._drop_last
            )
        msg = f"{type(self).__qualname__} instance doesn't have valid length"
        raise TypeError(msg)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(\n"
            f"  batch_size={self._batch_size},\n"
            f"  shuffle={self._shuffle},\n"
            f"  random_seed={self.random_seed},\n"
            f"  datapipe_or_batch={str_indent(self._datapipe_or_batch)},\n)"
        )

    @property
    def batch_size(self) -> int:
        r"""The batch size."""
        return self._batch_size

    @property
    def random_seed(self) -> int:
        r"""The random seed used to initialize the pseudo random
        generator."""
        return self._generator.initial_seed()
