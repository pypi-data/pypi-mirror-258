import functools

try:
    from IPython import get_ipython

    ip = get_ipython()
    if ip is None:
        pass
    else:
        pass
except:
    pass


from typing import Callable, Generator, Generic, Iterable, Union

from MelodieFuncFlow.functional import VARTYPE, MelodieFrozenGenerator, MelodieGenerator


class SkyGenerator(MelodieGenerator, Generic[VARTYPE]):
    pass


class SkyFrozenGenerator(MelodieFrozenGenerator, Generic[VARTYPE]):
    pass


def sky_generator(
    f: "Callable[..., Union[Generator[VARTYPE, None, None], SkyGenerator[VARTYPE]]]",
) -> "Callable[..., SkyGenerator[VARTYPE]]":
    @functools.wraps(
        f,
        assigned=(
            ("__module__", "__name__", "__qualname__", "__doc__", "__annotation__")
        ),
    )
    def inner(*args, **kwargs):
        return SkyGenerator(f(*args, **kwargs))

    return inner


def to_generator(it: Iterable[VARTYPE]) -> Generator[VARTYPE, None, None]:
    for item in it:
        yield item
