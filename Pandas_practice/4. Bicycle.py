# 데이터 불러오기
import pandas as pd

bicycle = pd.read_csv("Data/Fremont_Bridge_Bicycle_Counter.csv", encoding = 'utf-8-sig')

bicycle.iloc[145986] = bicycle.iloc[145986].fillna(0)
bicycle = bicycle.dropna()
bicycle[['Fremont Bridge Total','Fremont Bridge East Sidewalk','Fremont Bridge West Sidewalk']] = bicycle[['Fremont Bridge Total','Fremont Bridge East Sidewalk','Fremont Bridge West Sidewalk']].astype('int64')
bicycle['Date'] = pd.to_datetime(bicycle['Date'], format = "%m/%d/%Y %I:%M:%S %p", errors = 'raise')
bicycle = bicycle.sort_values(by = 'Date')
bicycle = bicycle.drop_duplicates(keep = 'first')

# 년 / 월 / 요일 / 시간 / 분기 받아오는 코드 작성
bicycle['year'] = bicycle['Date'].dt.year
bicycle['month'] = bicycle['Date'].dt.month
bicycle['weekday'] = bicycle['Date'].dt.weekday
bicycle['day'] = bicycle['Date'].dt.day
bicycle['hour'] = bicycle['Date'].dt.hour
bicycle['Quarter'] = bicycle['Date'].dt.quarter
bicycle_date = bicycle.copy()

bicycle_date = bicycle_date.sort_values(by = 'Date',ascending = True)


# 1.년도별 통계
bicycle_year = bicycle_date[['Fremont Bridge Total', 'Fremont Bridge East Sidewalk', 'Fremont Bridge West Sidewalk', 'year']].copy()
bicycle_year_19 = bicycle_year[bicycle_year['year'] == 2019]
bicycle_year_20 = bicycle_year[bicycle_year['year'] == 2020]
bicycle_year_21 = bicycle_year[bicycle_year['year'] == 2021]
bicycle_year_19_21 = pd.concat([bicycle_year_19, bicycle_year_20, bicycle_year_21])
bicycle_year_19_21 = bicycle_year_19_21[['Fremont Bridge Total', 'year']].copy()
bicycle_year_19_21 = bicycle_year_19_21.groupby('year').sum()
bicycle_year_19_21


# 2.월별 통계 - 2018~2021
bicycle_month = bicycle_date[['Fremont Bridge Total', 'Fremont Bridge East Sidewalk', 'Fremont Bridge West Sidewalk', 'year', 'month']].copy()
bicycle_year_18_month = bicycle_month[bicycle_month['year'] == 2018].copy()
bicycle_year_19_month = bicycle_month[bicycle_month['year'] == 2019].copy()
bicycle_year_20_month = bicycle_month[bicycle_month['year'] == 2020].copy()
bicycle_year_21_month = bicycle_month[bicycle_month['year'] == 2021].copy()
bicycle_year_18_21_month = pd.concat([bicycle_year_18_month, bicycle_year_19_month, 
                                      bicycle_year_20_month, bicycle_year_21_month]).copy()
bicycle_year_18_21_month = bicycle_year_18_21_month.groupby(['year','month']).aggregate({'Fremont Bridge Total' : 'sum'}).copy()
bicycle_year_18_21_month = bicycle_year_18_21_month.reset_index('month').copy()
bicycle_year_18_21_month

# 2.1. plotly로 시각화 - line 그래프]
import plotly.graph_objects as go
import plotly.offline as pyo
pyo.init_notebook_mode()

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x = bicycle_year_18_21_month['month'][:12], y = bicycle_year_18_21_month['Fremont Bridge Total'][:12], name = '2018'))

fig.add_trace(
    go.Scatter(
        x = bicycle_year_18_21_month['month'][12:24], y = bicycle_year_18_21_month['Fremont Bridge Total'][12:24], name = '2019'))

fig.add_trace(
    go.Scatter(
        x = bicycle_year_18_21_month['month'][24:36], y = bicycle_year_18_21_month['Fremont Bridge Total'][24:36], name = '2020'))

fig.add_trace(
    go.Scatter(
        x = bicycle_year_18_21_month['month'][-11:], y = bicycle_year_18_21_month['Fremont Bridge Total'][-11:], name = '2021'))

fig.update_layout(
    {
        'title' : {'text':'<b>Monthly Frement Bridge Total 2018 - 2021</b>', 'font' : {'size' : 25}, 'x':0.5, 'y':0.92},
        'xaxis' : {'showticklabels':True, 'dtick' : 1, 'title' : {'text' : 'Month', 'font': {'size' : 15}}},
        'yaxis' : {'showticklabels':True, 'title' : {'text' : 'Total', 'font': {'size' : 15}}}
    })

fig.show()


# 3.년도 / 월별  - East / West / Total 비교
bicycle_month = bicycle_date[['Fremont Bridge Total', 'Fremont Bridge East Sidewalk', 'Fremont Bridge West Sidewalk', 'year', 'month']].copy()
bicycle_EWT = bicycle_month
bicycle_EWT = bicycle_EWT.groupby(['year','month']).sum()
bicycle_EWT

# 3.1.iplot으로 시각화 - line 그래프
import chart_studio.plotly as py
import cufflinks as cf
cf.go_offline(connected=True)

bicycle_EWT.iplot(kind = 'scatter')

# 3.2 plotly로 시각화
bicycle_EWT_plotly = bicycle_EWT.reset_index()
bicycle_EWT_plotly[['year','month']] = bicycle_EWT_plotly[['year','month']].astype('str')
bicycle_EWT_plotly['Date'] = pd.to_datetime(bicycle_EWT_plotly['year'] + "-" + bicycle_EWT_plotly['month'])
bicycle_EWT_plotly = bicycle_EWT_plotly.sort_values('Date')
bicycle_EWT_plotly

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = bicycle_EWT_plotly['Date'], y = bicycle_EWT_plotly['Fremont Bridge Total'], name = 'Total'))

fig.add_trace(
    go.Scatter(
        x = bicycle_EWT_plotly['Date'], y = bicycle_EWT_plotly['Fremont Bridge West Sidewalk'], name = 'West'))

fig.add_trace(
    go.Scatter(
        x = bicycle_EWT_plotly['Date'], y = bicycle_EWT_plotly['Fremont Bridge East Sidewalk'], name = 'East'))

fig.show()


# 4.분기 당 시간별 자전거 이용자
bicycle_qurter = bicycle_date[['Quarter','hour','Fremont Bridge Total']].copy()
bicycle_qurter = bicycle_qurter.groupby(['Quarter','hour']).agg({'Fremont Bridge Total':'sum'}).copy()
bicycle_qurter = bicycle_qurter.reset_index().copy()
bicycle_qurter

# 4.1. iplot 으로 시각화 - Heatmap
bicycle_qurter.iplot(kind = 'heatmap', x = 'hour', y = 'Quarter', z = 'Fremont Bridge Total', colorscale = 'Reds')

# 4.2. plotly 로 시각화 - Heatmap
fig = go.Figure()
fig.add_trace(
    go.Heatmap(
        x = bicycle_qurter['hour'], y = bicycle_qurter['Quarter'], z = bicycle_qurter['Fremont Bridge Total'], colorscale='blues'))

fig.update_layout(
    {
        'title' : {'text':'<b>Heatmap - Quarter/Hour/Total</b>', 'font':{'size' : 25}, 'x':0.5, 'y':0.92},
        'xaxis' : {'showticklabels' : True, 'dtick' : 1, 'tick0' : 0, 'title' : {'text' : 'Hour', 'font' : {'size' : 20}}},
        'yaxis' : {'showticklabels' : True, 'title' : {'text' : 'Quarter', 'font' : {'size' : 20}}}
    })

fig.show()


# 5.자전거 이용자 통계
bicycle_week = bicycle_date[['weekday','hour','Fremont Bridge Total','Fremont Bridge East Sidewalk','Fremont Bridge West Sidewalk']]
bicycle_week = bicycle_week.groupby(['weekday','hour']).sum().copy()
bicycle_week = bicycle_week.reset_index().copy()
bicycle_week

# 5.1. weekday 열을 문자열로 바꿔주는 코드 작성
def weekday_func(row):
    if row['weekday'] == 0:
        row['weekday'] = 'Mon'
    elif row['weekday'] == 1:
        row['weekday'] = 'Tue'
    elif row['weekday'] == 2:
        row['weekday'] = 'Wed'
    elif row['weekday'] == 3:
        row['weekday'] = 'Thu'
    elif row['weekday'] == 4:
        row['weekday'] = 'Fri'
    elif row['weekday'] == 5:
        row['weekday'] = 'Sat'
    elif row['weekday'] == 6:
        row['weekday'] = 'Sun'
    return row
  
bicycle_week['weekday'] = bicycle_week.apply(weekday_func, axis = 1)
bicycle_week['weekday'] = pd.Categorical(bicycle_week['weekday'], categories=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], ordered = True)
bicycle_week = bicycle_week.sort_values(['weekday', 'hour'])
bicycle_week

# 5.2. 요일별 자전거 이용자
bicycle_weekday_day = bicycle_week.drop(columns = 'hour')
bicycle_weekday_day = bicycle_weekday_day.groupby('weekday').sum()
bicycle_weekday_day

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = bicycle_weekday_day.index, y = bicycle_weekday_day['Fremont Bridge Total'], name = 'Total'))

fig.add_trace(
    go.Scatter(
        x = bicycle_weekday_day.index, y = bicycle_weekday_day['Fremont Bridge East Sidewalk'], name = 'East'))

fig.add_trace(
    go.Scatter(
        x = bicycle_weekday_day.index, y = bicycle_weekday_day['Fremont Bridge West Sidewalk'], name = 'West'))
fig.show()


# 5.3. 주중 시간별 자전거 이용자
bicycle_weekday_hour = bicycle_week[:120].copy()
bicycle_weekday_hour = bicycle_weekday_hour.drop(columns = 'weekday')
bicycle_weekday_hour = bicycle_weekday_hour.groupby('hour').sum()
bicycle_weekday_hour

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = bicycle_weekday_hour.index, y = bicycle_weekday_hour['Fremont Bridge Total'], name = 'Total'))
fig.add_trace(
    go.Scatter(
        x = bicycle_weekday_hour.index, y = bicycle_weekday_hour['Fremont Bridge East Sidewalk'], name = 'East'))
fig.add_trace(
    go.Scatter(
        x = bicycle_weekday_hour.index, y = bicycle_weekday_hour['Fremont Bridge West Sidewalk'], name = 'West'))
fig.show()


# 5.4. 주말 시간별 자전거 이용자
bicycle_weekend_hour = bicycle_week[120:].copy()
bicycle_weekend_hour = bicycle_weekend_hour.drop(columns = 'weekday')
bicycle_weekend_hour = bicycle_weekend_hour.groupby('hour').sum()
bicycle_weekend_hour

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = bicycle_weekend_hour.index, y = bicycle_weekend_hour['Fremont Bridge Total'], name = 'Total'))
fig.add_trace(
    go.Scatter(
        x = bicycle_weekend_hour.index, y = bicycle_weekend_hour['Fremont Bridge East Sidewalk'], name = 'East'))
fig.add_trace(
    go.Scatter(
        x = bicycle_weekend_hour.index, y = bicycle_weekend_hour['Fremont Bridge West Sidewalk'], name = 'West'))
fig.show()
