import asyncio
from unittest import mock

import pytest

from aiocontext import async_contextmanager


@async_contextmanager
async def sleep_context(delay=0.0, result=None, start_callback=None, process_callback=None, end_callback=None):
    try:
        if start_callback:
            start_callback()
        yield await asyncio.sleep(delay=delay, result=result)
        if process_callback:
            process_callback()
    except Exception as e:
        if end_callback:
            if end_callback(e):
                raise
        else:
            raise
    else:
        if end_callback:
            end_callback()


@pytest.mark.asyncio
async def test_simple_expected_result():
    expected = 'Foo'
    async with sleep_context(result=expected) as result:
        assert result == expected


@pytest.mark.asyncio
async def test_simple_expected_result_double_call():
    expected = 'Foo'
    async with sleep_context(result=expected) as result:
        assert result == expected

    expected = 'Bar'
    async with sleep_context(result=expected) as result:
        assert result == expected


@pytest.mark.asyncio
async def test_error_after_yield():
    process_mock = mock.Mock()
    process_mock.side_effect = ValueError('Test')

    with pytest.raises(ValueError) as e:
        expected = 'Foo'
        async with sleep_context(result=expected, process_callback=process_mock) as result:
            assert result == expected

    assert e.value == process_mock.side_effect
    process_mock.assert_any_call()


@pytest.mark.asyncio
async def test_error_before_yield():
    start_mock = mock.Mock()
    start_mock.side_effect = ValueError('Test')

    with pytest.raises(ValueError) as e:
        async with sleep_context(start_callback=start_mock) as result:
            raise AssertionError('This code must not be run')

    assert e.value == start_mock.side_effect
    start_mock.assert_any_call()


@pytest.mark.asyncio
async def test_error_outside():
    process_callback = mock.Mock()
    end_callback = mock.Mock()
    end_callback.return_value = True

    error = ValueError('Test')

    with pytest.raises(type(error)) as e:
        async with sleep_context(process_callback=process_callback, end_callback=end_callback):
            raise error

    assert e.value == error
    assert end_callback.call_args[0][0] == error


@pytest.mark.asyncio
async def test_async_gen_no_yield():
    @async_contextmanager
    async def test():
        if False:
            yield
        return

    with pytest.raises(RuntimeError) as e:
        async with test():
            raise AssertionError('This code must not be run')
    assert str(e.value) == 'async generator didn\'t yield'


@pytest.mark.asyncio
async def test_several_yields():
    @async_contextmanager
    async def test():
        yield 'Foo'
        yield 'Bar'

    with pytest.raises(RuntimeError) as e:
        async with test() as result:
            assert result == 'Foo'

    assert str(e.value) == 'async generator didn\'t stop'


@pytest.mark.asyncio
async def test_several_suppress_outside_error():
    @async_contextmanager
    async def test():
        try:
            yield 'Foo'
        except:
            pass
        yield 'Bar'

    with pytest.raises(RuntimeError) as e:
        async with test() as result:
            assert result == 'Foo'
            raise ValueError('Test')
    assert str(e.value) == 'async generator didn\'t stop after throw()'


@pytest.mark.asyncio
async def test_raise_on_exception():
    @async_contextmanager
    async def test():
        try:
            yield 'Foo'
        except:
            raise TypeError('Test')

    with pytest.raises(TypeError) as e:
        async with test() as result:
            assert result == 'Foo'
            raise ValueError('Test')

    assert str(e.value) == 'Test'
