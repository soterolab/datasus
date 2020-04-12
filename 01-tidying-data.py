
import gc
import json
import pandas as pd
from tqdm import tqdm

file_path = '../../datasus.csv'
sim_json = './cols_sim.json'
pkl_file = 'datasus_tidy.pkl'

print('TIDYING datasus CSV:')

with open(sim_json, 'r') as file:
    sim = json.loads(file.read())

mapper = dict(zip(sim['cols'], sim['names']))

print('>>> Opening CSV...')
data = pd.read_csv(file_path, encoding='utf-8', index_col=0, dtype='object')

datasus = data.loc[:, sim['cols']].rename(columns=mapper)

del data
_ = gc.collect()

print('>>> Removing meaningless observations...')

unwanted = pd.Series(data=[False]*datasus.shape[0])

for col, vals in sim['unwanted'].items():
    unwanted = unwanted | datasus[col].isin(vals)

datasus = datasus.loc[~unwanted, :]

print('>>> Casting categorical columns...')

for cat_col in tqdm(sim['cat_cols']):
    categories = list(filter(lambda c: pd.notna(c), datasus[cat_col].unique()))
    cat_type = pd.CategoricalDtype(categories=categories)
    datasus[cat_col] = pd.Categorical(datasus[cat_col], dtype=cat_type)

print('>>> Casting numeric columns...')

for num_col in tqdm(sim['num_cols']):
    datasus[num_col] = pd.to_numeric(datasus[num_col], errors='coerce', downcast='float')

print('>>> Casting datetime columns...')

for dt_col in tqdm(sim['dt_cols']):
    datasus[dt_col] = pd.to_datetime(datasus[dt_col], errors='coerce', yearfirst=True, infer_datetime_format=True)

print('>>> Outputting tidy dataframe to a .pkl file...')

datasus.to_pickle(pkl_file, compression='zip')

print('DONE.')