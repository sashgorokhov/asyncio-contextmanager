# asyncio-contextmanager

[![PyPI version](https://badge.fury.io/py/asyncio-contextmanager.svg)](https://badge.fury.io/py/asyncio-contextmanager) [![GitHub release](https://img.shields.io/github/release/sashgorokhov/asyncio-contextmanager.svg)](https://github.com/sashgorokhov/asyncio-contextmanager) [![Build Status](https://travis-ci.org/sashgorokhov/asyncio-contextmanager.svg?branch=master)](https://travis-ci.org/sashgorokhov/asyncio-contextmanager) [![codecov](https://codecov.io/gh/sashgorokhov/asyncio-contextmanager/branch/master/graph/badge.svg)](https://codecov.io/gh/sashgorokhov/asyncio-contextmanager) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/sashgorokhov/asyncio-contextmanager/master/LICENSE)

Decorator that turns async generator functions into async context managers.


## Installation

Supported versions of python: **`3.6+`** (since async generators were introduced in python 3.6)

```shell
pip install asyncio-contextmanager
```

## Usage

Usage is straightforward and simple:
```python
from aiocontext import async_contextmanager

@async_contextmanager
async def foo():
    yield 'Foo!'
```