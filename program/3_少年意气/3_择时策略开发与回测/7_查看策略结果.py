"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
调用各个函数，查看策略结果
"""
import pandas as pd
from datetime import timedelta
from Signals import *
from Position import *
from Evaluate import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# =====手工设定策略参数
symbol = 'BTC-USDT_5m'
para = [400, 2, 0.05]

face_value = 0.01  # btc是0.01，不同的币种要进行不同的替换
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
leverage_rate = 3
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
rule_type = '15T'
drop_days = 10  # 币种刚刚上线10天内不交易


# =====读入数据
df = pd.read_hdf('%s.h5' % symbol, key='df')
# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df.reset_index(inplace=True, drop=True)


# =====转换为其他分钟数据
rule_type = '15T'
period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
    {'open': 'first',
     'high': 'max',
     'low': 'min',
     'close': 'last',
     'volume': 'sum',

     })
period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
period_df.reset_index(inplace=True)
df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]
df = df[df['candle_begin_time'] >= pd.to_datetime('2017-01-01')]
df.reset_index(inplace=True, drop=True)


# =====计算交易信号
# df = signal_simple_bolling2(df, para=para)
df = bolling_new(df, para=para)

# =====计算实际持仓
df = position_for_OKEx_future(df)




#431.8450453301607
#431.8450453301607
df.to_csv('b.csv')


# =====计算资金曲线
# 选取相关时间。币种上线10天之后的日期
t = df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
df = df[df['candle_begin_time'] > t]
# 计算资金曲线
df = equity_curve_for_OKEx_USDT_future_next_open(df, slippage=slippage, c_rate=c_rate, leverage_rate=leverage_rate,
                                                 face_value=face_value, min_margin_ratio=min_margin_ratio)
print(df)
print('策略最终收益：', df.iloc[-1]['equity_curve'])

