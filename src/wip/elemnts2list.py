import pandas as pd

outer_envelopes = []
inner_envelopes = []
this_transaction = []

transactional_envelopes = []
transaction_data = []

for row in elements:
    if row[0] in ['ISA', 'IEA']:
        outer_envelopes.append(row)

    elif row[0] in ['GS', 'GE']:
        inner_envelopes.append(row)

    else:
        if row[0] == 'ST':
            transactional_envelopes.append(row)
            this_transaction = [row]

        elif row[0] != 'SE':
            this_transaction.append(row)

        else:
            this_transaction.append(row)
            transactional_envelopes.append(this_transaction)

len(inner_envelopes)

this_transaction[1]
