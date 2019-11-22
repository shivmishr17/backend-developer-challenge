from .currency_manager import get_currency_exchange_rates, update_by_exchange_rate
import pandas as pd
import os


def process_data(data, base_currency):
    rates = get_currency_exchange_rates(base_currency)
    updated_data = _convert_currency(data, rates, base_currency)
    group_data = group_data_by_nonprofit(updated_data)
    # save final response csv.
    group_data.to_csv(os.path.join('uploads', 'response.csv'), index=None, header=True)


def group_data_by_nonprofit(input_data):
    groups = []
    group_data = input_data.groupby('Nonprofit')
    for nonprofit, data in group_data.groups.items():
        if nonprofit == 'Nonprofit':
            continue
        row_numbers = data.values
        total_amount = 0
        total_fee = 0
        for row_num in row_numbers:
            row = input_data.loc[row_num]
            total_fee += float(row['Fee'].replace(',', ''))
            total_amount += float(row['Donation Amount'])
        groups.append({'Nonprofit': nonprofit, 'Total Fee': total_fee, 'Total amount': total_amount,
                       'Number of Donations': len(row_numbers)})
    return pd.DataFrame(groups)


def _convert_currency(data, rates, base_currency):
    for row_num, currency in enumerate(data['Donation Currency']):
        try:
            if row_num == 0:
                continue
            row = data.loc[row_num]
            if row is None or row['Donation Amount'] == '':
                continue
            amount = row['Donation Amount']
            amount = amount.replace(',', '') if type(amount) is str else amount
            row['Donation Amount'] = update_by_exchange_rate(row['Donation Currency'],
                                                             amount, rates)
            row['Donation Currency'] = base_currency
        except Exception as e:
            print(e)
            continue
    return data
