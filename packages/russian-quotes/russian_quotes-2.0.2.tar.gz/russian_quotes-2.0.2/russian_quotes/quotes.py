import aiohttp
import requests
from . import exceptions
from typing import Union, Dict, Tuple, Literal

LANG = Literal['en', 'ru']
                
async def get_quote_async(lang: LANG = 'en', as_dict: bool = False) -> Union[Dict, Tuple]:
    """
    Get random quote on russian from forismatic API.

    Parameters:
        - lang `Literal['en', 'ru']`\n
            If \'en\' returns quote in English\n
            If \'ru\' returns quote in Russian
        - as_dict `bool`\n
            If True returns dict\n
            If False returns tuple

    Returns: `Union[Dict, Tuple]`

    Raises:
        `ServerError`
            Returns when server status isn\`t 200.

        `LanguageIsNotSupported`
            Returns when lang isn`t \'en\' or \'ru\'
    """
    if lang not in ['en', 'ru']:
        raise exceptions.LanguageIsNotSupported('This language is not supported (only \'en\' or \'ru\').')

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}') as response:
            if response.status == 200:
                data = await response.json()

                if as_dict:
                    return data

                return data['quoteText'], data['quoteAuthor']
            else:
                raise exceptions.ServerError(f'Server isn`t responding. Status code: {response.status}')
    
def get_quote(lang: LANG = "en", as_dict: bool = False) -> Union[Dict, Tuple]:
    """
    Get random quote on russian from forismatic API.

    Parameters:
        - lang `Literal['en', 'ru']`\n
            If \'en\' returns quote in English\n
            If \'ru\' returns quote in Russian
        - as_dict `bool`\n
            If True returns dict\n
            If False returns tuple

    Returns: `Union[Dict, Tuple]`

    Raises:
        `ServerError`
            Returns when server status isn\`t 200.

        `LanguageIsNotSupported`
            Returns when lang isn`t \'en\' or \'ru\'
    """
    if lang not in ['en', 'ru']:
        raise exceptions.LanguageIsNotSupported('This language is not supported (only \'en\' or \'ru\').')
    
    data = requests.get(f'https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}').json()

    if as_dict:
        return data

    return data['quoteText'], data['quoteAuthor']
