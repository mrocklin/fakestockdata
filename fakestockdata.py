from glob import glob
import os
import requests
import zipfile
import pandas as pd

# https://quantquote.com/historical-stock-data  Free Data tab
daily_csv_url = 'http://quantquote.com/files/quantquote_daily_sp500_83986.zip'

def download_daily():
    r = requests.get(daily_csv_url, stream=True)
    if not os.path.exists('data'):
        os.mkdir('data')

    with open(os.path.join('data', 'daily.zip'), 'wb') as f:
        for chunk in r.iter_content(chunk_size=2**12):
            f.write(chunk)

    f = zipfile.ZipFile(os.path.join('data', 'daily.zip'),
                        path=os.path.join('data', 'daily'))

    f.extractall()

columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']

def load_file(fn):
    return pd.read_csv(fn,
                     parse_dates=['date'],
                     infer_datetime_format=True,
                     header=None, index_col='date',
                     compression='bz2' if fn.endswith('bz2') else None,
                     names=columns).drop('time', axis=1)


import numpy as np
def generate_day(date, open, high, low, close, volume,
                 freq=pd.Timedelta(seconds=60)):
    time = pd.date_range(date + pd.Timedelta(hours=9),
                         date + pd.Timedelta(hours=5 + 12),
                         freq=freq / 5, name='timestamp')
    n = len(time)
    while True:
        values = (np.random.random(n) - 0.5).cumsum()
        values *= (high - low) / (values.max() - values.min())  # scale
        values += np.linspace(open - values[0], close - values[-1],
                              len(values))  # endpoints
        assert np.allclose(open, values[0])
        assert np.allclose(close, values[-1])

        mx = max(close, open)
        mn = min(close, open)
        ind = values > mx
        values[ind] = (values[ind] - mx) * (high - mx) / (values.max() - mx) + mx
        ind = values < mn
        values[ind] = (values[ind] - mn) * (low - mn) / (values.min() - mn) + mn
        if (np.allclose(values.max(), high) and  # The process fails if min/max
            np.allclose(values.min(), low)):     # are the same as open close
            break                                # this is pretty rare though

    s = pd.Series(values.round(3), index=time)
    rs = s.resample(freq)
    # TODO: add in volume
    return pd.DataFrame({'open': rs.first(),
                         'close': rs.last(),
                         'high': rs.max(),
                         'low': rs.min()})


def generate_stock(fn, freq=pd.Timedelta(seconds=60)):
    fn2 = os.path.split(fn)[1]
    sym = fn2[len('table_'):fn2.find('.csv')]
    if not os.path.exists(os.path.join('data', 'minute')):
        os.mkdir(os.path.join('data', 'minute'))
    if not os.path.exists(os.path.join('data', 'minute', sym)):
        os.mkdir(os.path.join('data', 'minute', sym))

    df = load_file(fn)
    for date, rec in df.to_dict(orient='index').items():
        df2 = generate_day(date, freq=freq, **rec)
        fn2 = os.path.join('data', 'minute', sym, str(date).replace(' ', 'T') + '.csv')
        df2.to_csv(fn2)


def generate_stocks(freq=pd.Timedelta(seconds=60)):
    from concurrent.futures import ProcessPoolExecutor, wait
    e = ProcessPoolExecutor()
    filenames = sorted(glob(os.path.join('data', 'daily', '*')))

    futures = [e.submit(generate_stock, fn, freq=freq) for fn in filenames]
    wait(futures)
