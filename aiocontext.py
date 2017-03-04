import functools
import inspect
import sys

__all__ = ['async_contextmanager']


class _AsyncContextManager(object):
    def __init__(self, func, args, kwargs):
        if not inspect.isasyncgenfunction(func):
            raise TypeError('%s is not async generator function' % func)
        self.async_generator = func(*args, **kwargs)

    async def __aenter__(self):
        try:
            return await self.async_generator.__anext__()
        except StopAsyncIteration as e:
            raise RuntimeError("async generator didn't yield") from None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                await self.async_generator.__anext__()
            except StopAsyncIteration:
                return
            else:
                raise RuntimeError("async generator didn't stop")
        else:
            if exc_val is None:
                exc_val = exc_type()
            try:
                await self.async_generator.athrow(exc_type, exc_val, exc_tb)
                raise RuntimeError("async generator didn't stop after throw()")
            except StopAsyncIteration as exc:
                return exc is not exc_val
            except RuntimeError as exc:
                if exc is exc_val:
                    return False
                if exc.__cause__ is exc_val:
                    return False
                raise
            except:
                if sys.exc_info()[1] is not exc_val:
                    raise


def async_contextmanager(func):
    """
    @async_contextmanager decorator.

    Typical usage:

        @async_contextmanager
        async def some_async_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>

    This makes this:

        async with some_async_generator(<arguments>) as <variable>:
            <body>

    equivalent to this:

        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _AsyncContextManager(func, args, kwargs)

    return wrapper
