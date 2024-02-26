from functools import wraps
from itertools import cycle
from itertools import repeat
import logging
import time
import typing as t


logger = logging.getLogger(__name__)


T = t.TypeVar('T')
Ts = t.Union[t.Type[T], tuple[t.Type[T], ...]]

DelaysT = t.Iterator[float]


def retry(
    retries=0,
    *,
    delays: DelaysT = repeat(0),
    exceptions: Ts[Exception] = Exception,
    exception_cb: t.Callable[[int, Exception], None] = lambda i, e: logger.warning(
        f'retry {i:}: {e = }'
    ),
):
    delays = cycle(delays)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for i in range(1, retries + 1):
                try:
                    result = f(*args, **kwargs)
                except exceptions as e:
                    exception_cb(i, e)
                    if i == retries:
                        raise
                    time.sleep(next(delays))
                except Exception:
                    raise
                else:
                    return result

        return wrapper

    return decorator


if __name__ == '__main__':

    @retry(14, exceptions=(ValueError, ZeroDivisionError))
    def f():
        1 / 0  # type: ignore[reportUnusedExpression]

    f()
