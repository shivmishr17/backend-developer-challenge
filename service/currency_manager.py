import requests

# URL = 'https://api.exchangeratesapi.io/latest'
URL = 'http://data.fixer.io/api/latest?access_key=41194289795b91275f7665e4511fdef4'


def get_currency_exchange_rates(base):
    response = requests.get(URL)
    if response.status_code == 200:
        body = response.json()
        return _update_rates_with_base(base, body)


# to handle free service issues.
def _update_rates_with_base(base, body):
    current_base = body['base']
    if current_base == base:
        return body['rates']
    else:
        exchange_rate = 1/body['rates'][base]
        rates = {}
        for k, v in body['rates'].items():
            rates[k] = v * exchange_rate
        return rates


def update_by_exchange_rate(current_currency, value, rates):
    factor = rates[current_currency]
    return float(value) / factor
