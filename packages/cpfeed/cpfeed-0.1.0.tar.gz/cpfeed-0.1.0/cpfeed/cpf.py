from typing_extensions import Annotated

import requests
import typer

from .errors import CoinGeckoAPIError, InvalidCoinError, InvalidCurrencyError, ERROR_MESSAGES


app = typer.Typer()


@app.command()
def get_price(
    token_name: Annotated[str, typer.Argument(help="Valid token name in full e.g Bitcoin")],
    fiat_currency: Annotated[str, typer.Argument(help="Valid fiat currency e.g EUR")] = "USD"
  ):
    """
    cpfeed (short for Crypto Price Feed) is a Python package for fetching cryptocurrency prices from the CoinGecko API.
    """
    token_name, fiat_currency = token_name.lower().strip(), fiat_currency.lower().strip()
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={token_name}&vs_currencies={fiat_currency}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if token_name not in data:
            raise InvalidCoinError(f'Invalid coin ID: {token_name}')
        if fiat_currency not in data[token_name]:
            raise InvalidCurrencyError(f'Invalid fiat_currency: {fiat_currency}')

        price = data[token_name][fiat_currency]
        typer.echo(f'The price of {token_name.title()} in {fiat_currency.upper()} is {price:,}')

    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code
        if status_code in ERROR_MESSAGES:
            raise CoinGeckoAPIError(ERROR_MESSAGES[status_code])
    except InvalidCoinError as coin_err:
        raise coin_err
    except InvalidCurrencyError as curr_err:
        raise curr_err
    except Exception as e:
        typer.echo(f'An error occurred: {e}')
