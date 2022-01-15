import pandas as pd
birth = pd.read_csv("Data/births.csv", encoding = 'utf-8-sig')

birth_1988 = birth[:15067]

birth_1988_F = birth_1988[birth_1988['gender'] == 'F'].copy()
birth_1988_F = birth_1988_F.groupby(by = ['year', 'month']).aggregate({'births' : 'sum'})
birth_1988_F = birth_1988_F.reset_index()

birth_1988_M = birth_1988[birth_1988['gender'] == 'M'].copy()
birth_1988_M = birth_1988_M.groupby(by = ['year', 'month']).aggregate({'births' : 'sum'})
birth_1988_M = birth_1988_M.reset_index()

birth_1989 = birth[15067:]

birth_1989_F = birth_1989[birth_1989['gender']=="F"].copy()
birth_1989_F = birth_1989_F[['year','month','births']].copy()

birth_1989_M = birth_1989[birth_1989['gender']=="M"].copy()
birth_1989_M = birth_1989_M[['year','month','births']].copy()

birth_F = pd.concat([birth_1988_F, birth_1989_F])
birth_M = pd.concat([birth_1988_M, birth_1989_M])

birth_F_year = birth_F.groupby('year').aggregate({'births' : 'sum'})
birth_M_year = birth_M.groupby('year').aggregate({'births' : 'sum'})
birth_year = pd.merge(birth_F_year, birth_M_year, on = 'year', how = 'inner')
birth_year.columns = ['births_F', 'births_M']

import plotly.graph_objects as go
import plotly.offline as pyo
pyo.init_notebook_mode()

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = birth_year.index, y = birth_year['births_F'], name='Female',
        text = birth_year['births_F'], texttemplate = '%{text:,}'
    ))

fig.add_trace(
    go.Scatter(
        x = birth_year.index, y = birth_year['births_M'], name = 'Male',
        text = birth_year['births_M'], texttemplate = '%{text:,}', textfont= dict(color = 'white')
    ))

fig.update_layout(
    {
        'title' : {'text' : '<b>Female/Male births per year</b>', 'font' : {'size' : 25}, 'x' : 0.5, 'y': 0.9},
        'xaxis' : {'showticklabels' : True, 'dtick' : 1, 'title' : {'text' : 'year', 'font' : {'size' : 20}}},
        'yaxis' : {'showticklabels' : True, 'tick0' : '1M', 'title' : {'text' : 'births', 'font' : {'size' : 20}}},
        
        'showlegend' : True

    })
fig.show()


birth_date = birth.dropna().copy()
birth_date = pd.pivot_table(birth_date, index = ['year','month', 'day'], values = ['births'], aggfunc={'births' : 'sum'})
birth_date = birth_date.reset_index()
birth_date[['day']] = birth_date[['day']].astype('int64')

import numpy as np
quartiles = np.percentile(birth_date['births'], [25,50,75])
mu = quartiles[1]
sig = 0.74 * (quartiles[2] - quartiles[0])
birth_date = birth_date.query('(births > @mu - 5*@sig) & (births < @mu + 5*@sig)')

birth_date = birth_date.astype('str')
birth_date['date'] = birth_date[['year', 'month', 'day']].apply('-'.join, axis = 1)
birth_date = birth_date[['date', 'births']].copy()
birth_date['date'] = pd.to_datetime(birth_date['date'], format = '%Y-%m-%d', errors = 'raise')

birth_date['year'] = birth_date['date'].dt.year
birth_date['month'] = birth_date['date'].dt.month
birth_date['day'] = birth_date['date'].dt.day
birth_date['weekday'] = birth_date['date'].dt.weekday

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
  
birth_date = birth_date.apply(weekday_func, axis = 1)

def decade_func(row):
    if row['year'] // 10 == 196:
        row['decade'] = 1960
    elif row['year'] // 10 == 197:
        row['decade'] = 1970
    elif row['year'] // 10 == 198:
        row['decade'] = 1980
    return row
  
birth_date = birth_date.apply(decade_func, axis = 1)
birth_date = birth_date[['decade', 'weekday', 'births']].copy()
birth_date['births'] = birth_date['births'].astype('int64')
birth_decade_weekday = birth_date.groupby(['decade','weekday']).sum()
birth_decade_weekday = birth_decade_weekday.reset_index()
birth_decade_weekday['decade'] = pd.Categorical(birth_decade_weekday['decade'], categories=[1960,1970,1980], ordered = True)
birth_decade_weekday['weekday'] = pd.Categorical(birth_decade_weekday['weekday'], categories=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], ordered = True)
birth_decade_weekday = birth_decade_weekday.sort_values(['decade','weekday'])
birth_decade_weekday = birth_decade_weekday.set_index('decade')

birth_1960 = birth_decade_weekday[birth_decade_weekday.index == 1960]
birth_1970 = birth_decade_weekday[birth_decade_weekday.index == 1970]
birth_1980 = birth_decade_weekday[birth_decade_weekday.index == 1980]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = birth_1970['weekday'], y = birth_1970['births'], name = '1970'))

fig.add_trace(
    go.Scatter(
        x = birth_1980['weekday'], y = birth_1980['births'], name = '1980'))

fig.update_layout(
{
    'title' : {'text' : '<b>Births by Weekday in 1970 / 1980</b>', 'font' : {'size' : 25}, 'x' : 0.5, 'y' : 0.92},
    'showlegend' : True,
    'xaxis' : {'showticklabels' : True, 'title' : {'text' : 'Weekday', 'font' : {'size' : 15}}},
    'yaxis' : {'showticklabels' : True, 'title' : {'text' : 'Births', 'font' : {'size' : 15}}}
})
fig.show()


birth_1969 = birth[birth['year'] == 1969]
birth_1969['day'] = birth_1969['day'].astype('int64')

import numpy as np
quartiles = np.percentile(birth_1969['births'], [25,50,75])
mu = quartiles[1]
sig = 0.74 * (quartiles[2] - quartiles[0])
birth_1969 = birth_1969.query('(births > @mu - 5*@sig) & (births < @mu + 5*@sig)')

birth_1969 = birth_1969.astype('str')
birth_1969['date'] = birth_1969[['year','month','day']].apply('-'.join, axis = 1)
birth_1969['births'] = birth_1969['births'].astype('int64')

birth_1969 = birth_1969.groupby('date').aggregate({'births' : 'sum'})
birth_1969 = birth_1969.reset_index()
birth_1969 = birth_1969.sort_values('date')
birth_1969['date'] = pd.to_datetime(birth_1969['date'], format = '%Y-%m-%d', errors = 'raise')
birth_1969 = birth_1969.set_index('date')
birth_1969 = birth_1969.sort_index()


fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = birth_1969.index, y = birth_1969['births'], marker_color = '#025918'))

fig.update_layout(
{
    'title' : {'text':'<b>Births in 1969</b>', 'font':{'size':25}, 'x':0.5, 'y':0.92},
    'xaxis' : {'showticklabels':True, 'dtick':'M1', 'tickfont' : {'size':15}, 'title' : {'text':'Date', 'font':{'size':20}}},
    'yaxis' : {'showticklabels':True, 'tickfont' : {'size':15}, 'title' : {'text':'Births', 'font':{'size':20}}},
    'template':'presentation'
})

fig.add_annotation(
    x = '1969-12-30', y = 12250,
    
    arrowcolor='#025918',
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    
    text = 'MAX : 1969-12-30,12232',
    font = dict(size = 13, color = 'white'),
    
    bordercolor='#025918',
    borderpad=4,
    borderwidth=2,
    
    ax = 20, ay = -40,
    align = 'center',
    bgcolor = '#025918',
    opacity = 0.8
    )

fig.add_annotation(
    x = '1969-4-20', y = 7930,
    
    arrowcolor='#025918',
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    
    text = 'MIN : 1969-4-20, 7928',
    font = dict(size = 13, color = 'white'),
    
    bordercolor='#025918',
    borderpad=4,
    borderwidth=2,
    
    ax = 20, ay = 50,
    align = 'center',
    bgcolor = '#025918',
    opacity = 0.8
    )

fig.show()
