
import pandas as pd
import ccxt
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

okex = ccxt.okex()

begin_date = '2021-02-26T00:00:00Z'  # 手工设定开始时间
end_date = '2021-02-27T00:00:00Z'  # 手工设定结束时间
symbol_list = ["BTC-USD-210305", "BTC-USDT-210305"]
time_interval = 300

date_list = []
date = pd.to_datetime(begin_date)


# 遍历时间周期

for symbol in symbol_list:

    path = 'D:/xbx-coin-2020/data/futures_candle_data'

    params = {
        'instrument_id': symbol,
        'granularity': time_interval,
        'start': begin_date,
        'end': end_date
    }  # 需要对着文档，使用okex独有的参数
    data = okex.futuresGetInstrumentsInstrumentIdCandles(params)

    df = pd.DataFrame(data, dtype=float)

    # ===合并整理数据
    df.rename(columns={0: 'DATE', 1: 'open', 2: 'high',
                       3: 'low', 4: 'close', 5: 'volume'}, inplace=True)  # 重命名

    df['candle_begin_time'] = pd.to_datetime(df['DATE'])  # 整理时间
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]  # 整理列的顺序

    df.sort_values('candle_begin_time', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # ===保存数据到文件
    # 创建交易所文件夹
    path = os.path.join(path)
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建spot文件夹
    path = os.path.join(path, 'futures')
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建日期文件夹
    path = os.path.join(path, str(pd.to_datetime(begin_date).date()))
    if os.path.exists(path) is False:
        os.mkdir(path)

    # 拼接文件目录
    file_name = symbol + '.csv'
    path = os.path.join(path, file_name)
    # 保存数据
    df.to_csv(path, index=False)