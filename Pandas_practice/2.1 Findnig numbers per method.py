import pandas as pd
import seaborn as sns
planets = sns.load_dataset('planets')

# 전처리
planets_number = planets[['method', 'number']].copy() 
planets_number = planets_number.groupby('method').sum().sort_values('number', ascending=False)

# 1.iplot 시각화
import chart_studio.plotly as py
import cufflinks as cf
cf.go_offline(connected = True)

# 1.1.막대 그래프
layout = {
    'title' : {'text' : '<b>Findnig numbers per method</b>',
               'font' : {'size' : 25},
               'x' : 0.5, 'y' : 0.9
              },
    
    'xaxis' : {'showticklabels' : True,
              'title' : {'text' : 'Method', 'font' : {'size' : 20}}},
    
    'yaxis' : {'showticklabels' : True,
              'dtick' : '100',
              'title' : {'text' : 'numbers', 'font' : {'size' : 20}}}   
}

planets_number.iplot(kind = 'bar', theme = 'white', layout = layout)

# 1.2.원 그래프
planets_number_df = planets[['method', 'number']]
planets_number_df.iplot(kind = 'pie', theme = 'white', labels = 'method', values = 'number')


# 2.plotly 시각화 
import plotly.graph_objects as go
import plotly.offline as pyo
pyo.init_notebook_mode()

import plotly. io as pio
pio.templates

# 2.1.막대 그래프
fig = go.Figure()
fig.add_trace(
    go.Bar(
    x = planets_number.index, y = planets_number['number']))

fig.update_layout(
    {
    'title' : {'text' : '<b>Findnig numbers per method</b>', 'font' : {'size' : 25}, 'x' : 0.5, 'y' : 0.9},
    'xaxis' : {'showticklabels' : True, 'title' : {'text' : 'Method', 'font' : {'size' : 15}}},
    'yaxis' : {'showticklabels' : True, 'dtick' : 100, 'title' : {'text' : 'Number', 'font' : {'size' : 15}}},
    'template' : 'plotly_white'
    })

fig.show()       

# 2.2. 원 그래프
fig = go.Figure()
fig.add_trace(
    go.Pie(
        labels = planets_number_df['method'], values = planets_number_df['number']
    ))

fig.show()
