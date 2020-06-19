import streamlit as st
import pandas as pd
from pathlib import Path

#Выгружаем тикеры из файла
@st.cache
def load_tickers():
    res = []
    file = open(Path('data')/'tickers', 'r')
    line = file.readline()
    while line != '':
        res.append(line)
        line = file.readline()
    return res


data_load_state = st.text('Starting loading tickers...')
#Выгружаем тикеры в переменную
tickers = load_tickers()
data_load_state.text("Tickers ready. Amount of tickers " + str(len(tickers)))


#Выгружаем данные по всем тикерам, что мы нашли.
@st.cache
def load_data():
    res = []
    for tic in tickers:
        res.append(pd.read_csv(Path('data')/(tic.strip() + '.csv'), index_col=0).rename(columns={'Value':'Price'}))
    return res


#Выгружаем данные из кэша
true_tic = tickers
tables = load_data()
data_load_state.text("Complete. Amount of loaded tickers  " + str(len(tables)))

#Теперь получаем значение нужного тикера и строим график
cur_tic = st.selectbox('Find data to :', true_tic)
cur_num = -1
for i in range(len(true_tic)):
    if cur_tic == true_tic[i]:
        cur_num = i
st.line_chart(tables[cur_num])


#Добавляем возможность получить сырые данные и скрыть их
def show():
    if st.button('Show raw data'):
        st.subheader('Raw data')
        st.dataframe(tables[cur_num])
        hide()


def hide():
    if st.button('Hide raw data'):
        show()


show()

#Теперь получаем возможность построить 2 графика на 1
def j(i, j):
    df1 = tables[i]
    df2 = tables[j]
    return df1.join(df2, how='inner', lsuffix='_'+tickers[i], rsuffix='_'+tickers[j])


comp_tic1 = st.selectbox('Compare data :', true_tic)
comp_tic2 = st.selectbox('With :', true_tic)
cur_num1 = -1
cur_num2 = -1
for i in range(len(true_tic)):
    if comp_tic1 == true_tic[i]:
        cur_num1 = i
    if comp_tic2 == true_tic[i]:
        cur_num2 = i
chart_data = j(cur_num1, cur_num2)
st.line_chart(chart_data)
