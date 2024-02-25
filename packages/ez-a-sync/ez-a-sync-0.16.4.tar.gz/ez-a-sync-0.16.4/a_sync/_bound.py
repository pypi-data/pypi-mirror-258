# mypy: disable-error-code=valid-type
# mypy: disable-error-code=misc
import functools
from inspect import isawaitable

from a_sync import _helpers
from a_sync._typing import *
from a_sync.decorator import a_sync as unbound_a_sync
from a_sync.modified import ASyncFunction
from a_sync.property import (AsyncCachedPropertyDescriptor,
                             AsyncPropertyDescriptor)

if TYPE_CHECKING:
    from a_sync.abstract import ASyncABC


def _clean_default_from_modifiers(
    coro_fn: AsyncBoundMethod[P, T],  # type: ignore [misc]
    modifiers: ModifierKwargs,
):
    # NOTE: We set the default here manually because the default set by the user will be used later in the code to determine whether to await.
    force_await = None
    if not asyncio.iscoroutinefunction(coro_fn) and not isinstance(coro_fn, ASyncFunction):
        if 'default' not in modifiers or modifiers['default'] != 'async':
            if 'default' in modifiers and modifiers['default'] == 'sync':
                force_await = True
            modifiers['default'] = 'async'
    return modifiers, force_await

            
def _wrap_bound_method(
    coro_fn: AsyncBoundMethod[P, T],
    **modifiers: Unpack[ModifierKwargs]
) -> AsyncBoundMethod[P, T]:
    from a_sync.abstract import ASyncABC
    
    # First we unwrap the coro_fn and rewrap it so overriding flag kwargs are handled automagically.
    if isinstance(coro_fn, ASyncFunction):
        coro_fn = coro_fn.__wrapped__
    
    modifiers, _force_await = _clean_default_from_modifiers(coro_fn, modifiers)
    
    wrapped_coro_fn: AsyncBoundMethod[P, T] = ASyncFunction(coro_fn, **modifiers)  # type: ignore [arg-type, valid-type, misc]

    @functools.wraps(coro_fn)
    def bound_a_sync_wrap(self: ASyncABC, *args: P.args, **kwargs: P.kwargs) -> T:  # type: ignore [name-defined]
        if not isinstance(self, ASyncABC):
            raise RuntimeError(f"{self} must be an instance of a class that inherits from ASyncABC.")
        # This could either be a coroutine or a return value from an awaited coroutine,
        #   depending on if an overriding flag kwarg was passed into the function call.
        retval = coro = wrapped_coro_fn(self, *args, **kwargs)
        if not isawaitable(retval):
            # The coroutine was already awaited due to the use of an overriding flag kwarg.
            # We can return the value.
            return retval  # type: ignore [return-value]
        # The awaitable was not awaited, so now we need to check the flag as defined on 'self' and await if appropriate.
        return _helpers._await(coro) if self.__a_sync_should_await__(kwargs, force=_force_await) else coro  # type: ignore [call-overload, return-value]
    return bound_a_sync_wrap

class _PropertyGetter(Awaitable[T]):
    def __init__(self, coro: Awaitable[T], property: Union[AsyncPropertyDescriptor[T], AsyncCachedPropertyDescriptor[T]]):
        self._coro = coro
        self._property = property
    def __repr__(self) -> str:
        return f"<_PropertyGetter for {self._property}._get at {hex(id(self))}>"
    def __await__(self) -> Generator[Any, None, T]:
        return self._coro.__await__()

@overload
def _wrap_property(
    async_property: AsyncPropertyDescriptor[T],
    **modifiers: Unpack[ModifierKwargs]
) -> AsyncPropertyDescriptor[T]:...

@overload
def _wrap_property(
    async_property: AsyncCachedPropertyDescriptor[T],
    **modifiers: Unpack[ModifierKwargs]
) -> AsyncCachedPropertyDescriptor:...

def _wrap_property(
    async_property: Union[AsyncPropertyDescriptor[T], AsyncCachedPropertyDescriptor[T]],
    **modifiers: Unpack[ModifierKwargs]
) -> Tuple[Property[T], HiddenMethod[T]]:
    if not isinstance(async_property, (AsyncPropertyDescriptor, AsyncCachedPropertyDescriptor)):
        raise TypeError(f"{async_property} must be one of: AsyncPropertyDescriptor, AsyncCachedPropertyDescriptor")

    from a_sync.abstract import ASyncABC

    async_property.hidden_method_name = f"__{async_property.field_name}__"
    
    modifiers, _force_await = _clean_default_from_modifiers(async_property, modifiers)
    
    @unbound_a_sync(**modifiers)
    async def _get(instance: ASyncABC) -> T:
        return await async_property.__get__(instance, async_property)
    
    @functools.wraps(async_property)
    def a_sync_method(self: ASyncABC, **kwargs) -> T:
        if not isinstance(self, ASyncABC):
            raise RuntimeError(f"{self} must be an instance of a class that inherits from ASyncABC.")
        awaitable = _PropertyGetter(_get(self), async_property)
        return _helpers._await(awaitable) if self.__a_sync_should_await__(kwargs, force=_force_await) else awaitable
    
    @property  # type: ignore [misc]
    @functools.wraps(async_property)
    def a_sync_property(self: ASyncABC) -> T:
        coro = getattr(self, async_property.hidden_method_name)(sync=False)
        return _helpers._await(coro) if self.__a_sync_should_await__({}, force=_force_await) else coro
    
    return a_sync_property, a_sync_method
