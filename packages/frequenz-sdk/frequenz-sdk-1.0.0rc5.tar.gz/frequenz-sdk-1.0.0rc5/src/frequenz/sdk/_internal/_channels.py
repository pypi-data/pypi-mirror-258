# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""General purpose classes for use with channels."""

import abc
import asyncio
import typing

from frequenz.channels import Receiver

T = typing.TypeVar("T")


class ReceiverFetcher(typing.Generic[T], typing.Protocol):
    """An interface that just exposes a `new_receiver` method."""

    @abc.abstractmethod
    def new_receiver(self, *, maxsize: int = 50) -> Receiver[T]:
        """Get a receiver from the channel.

        Args:
            maxsize: The maximum size of the receiver.

        Returns:
            A receiver instance.
        """


class _Sentinel:
    """A sentinel to denote that no value has been received yet."""


class LatestValueCache(typing.Generic[T]):
    """A cache that stores the latest value in a receiver."""

    def __init__(self, receiver: Receiver[T]) -> None:
        """Create a new cache.

        Args:
            receiver: The receiver to cache.
        """
        self._receiver = receiver
        self._latest_value: T | _Sentinel = _Sentinel()
        self._task = asyncio.create_task(self._run())

    def get(self) -> T:
        """Return the latest value that has been received.

        This raises a `ValueError` if no value has been received yet. Use `has_value` to
        check whether a value has been received yet, before trying to access the value,
        to avoid the exception.

        Returns:
            The latest value that has been received.

        Raises:
            ValueError: If no value has been received yet.
        """
        if isinstance(self._latest_value, _Sentinel):
            raise ValueError("No value has been received yet.")
        return self._latest_value

    def has_value(self) -> bool:
        """Check whether a value has been received yet.

        Returns:
            `True` if a value has been received, `False` otherwise.
        """
        return not isinstance(self._latest_value, _Sentinel)

    async def _run(self) -> None:
        async for value in self._receiver:
            self._latest_value = value
