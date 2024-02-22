"""
Russian Quotes
~~~~~~~~~~~~~~

Quotes of famous people on russian. Async & Sync.

Unofficial Forismatic API Wrapper.

&copy; r-liner 2023-present
:license: MIT

## Examples

### Sync

```py
from russian_quotes import get_quote

quote_author, quote_text = get_quote()

print(f'{quote_author}-{quote_text}')

>>> The undertaking of a new action brings new strength. -Richard Evans
```

### Async

```py
from russian_quotes import get_quote_async
import asyncio

quote_author, quote_text = asyncio.run(get_quote_async())

print(f'{quote_author}-{quote_text}')

>>> Every action of our lives touches on some chord that will vibrate in eternity. -Edwin Chapin
```
"""

from .quotes import get_quote, get_quote_async
from .exceptions import ServerError, LanguageIsNotSupported
from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __license__,
    __title__,
    __description__,
    __url__,
    __version__,
)