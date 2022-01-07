# 데이터 불러오기
import pandas as pd
import seaborn as sns
planets = sns.load_dataset('planets')

# 전처리
planets[planets['method'] == "Radial Velocity"].sort_values('year')
planets_number_year = planets[['method', 'number', 'year']].copy()
planets_number_year_Radial =  planets_number_year[planets_number_year['method']=='Radial Velocity']
del planets_number_year_Radial['method']
planets_number_year_Radial = planets_number_year_Radial.groupby('year').sum().sort_index()
planets_number_year_Radial = planets_number_year_Radial[1:]

# 1.iplot
import chart_studio.plotly as py
import cufflinks as cf
cf.go_offline(connected = True)

# 1.1. 막대 그래프
layout = {
    'title' : {'text' : '<b>Finding numbers per year in Redial Velocity since 1995</b>', 'font' : {'size' : 25}, 'x' : 0.5, 'y' : 0.9},
    'xaxis' : {'showticklabels' : True, 'dtick': 1, 'title' : {'text' : 'Year', 'font' : {'size' : 15}}},
    'yaxis' : {'showticklabels' : True, 'title' : {'text' : 'Number', 'font' : {'size' : 15}}}
}

planets_number_year_Radial.iplot(kind = 'scatter', mode = 'lines+markers', layout = layout)


# 2.plotly
import plotly.graph_objects as go
import plotly.offline as pyo
pyo.init_notebook_mode()

# 2.1.막대 그래프
colors = ['#03658C',] * len(planets_number_year_Radial.index)
colors[16] = '#F29F05'

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x = planets_number_year_Radial.index, y = planets_number_year_Radial['number'],
        text = planets_number_year_Radial['number'], 
        textposition='inside', texttemplate = '%{text}', textfont=dict(color = 'white', size = 10),
        marker_color = colors))

fig.update_layout({
    'title' : {'text' : '<b>Finding numbers per year in Redial Velocity since 1995</b>', 'font' : {'size' : 25}, 'x' : 0.5, 'y' : 0.9},
    'xaxis' : {'showticklabels' : True, 'dtick' : 1, 'title' : {'text' : 'Year', 'font' : {'size' :  15}}},
    'yaxis' : {'showticklabels' : True, 'title' : {'text' : 'Year', 'font' : {'size' :  15}}},
    'template' : 'plotly_white'
})

fig.add_annotation(
            x = 2011, y = 180,
            text = '<b>2011 : 176</b>',
            showarrow = True,
            font = {'size' : 10, 'color' : '#ffffff'},
            align = 'center',
            arrowhead = 2,
            arrowsize = 1,
            arrowwidth = 2,
            arrowcolor = '#F29F05',
            ax = 40, ay = -30,
            bordercolor = '#F29F05',
            borderwidth = 2,
            borderpad = 4,
            bgcolor = '#F29F05',
            opacity = 0.8
)
fig.show()

# 2.2.Scatter 그래프
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = planets_number_year_Radial.index, y = planets_number_year_Radial['number'], mode = 'lines+markers'))

fig.update_layout({
    'title' : {'text' : '<b>Finding numbers per year in Redial Velocity since 1995</b>', 'font' : {'size' : 25}, 'x' : 0.5, 'y' : 0.9},
    'xaxis' : {'showticklabels' : True, 'dtick' : 1, 'title' : {'text' : 'Year', 'font' : {'size' :  15}}},
    'yaxis' : {'showticklabels' : True, 'title' : {'text' : 'Year', 'font' : {'size' :  15}}},
    'template' : 'ggplot2'
})

fig.add_annotation(
            x = 2011, y = 180,
    
            text = '<b>2011 : 176</b>',
            showarrow = True,
            font = {'size' : 10, 'color' : '#ffffff'},
    
            align = 'center',
            arrowhead = 2,
            arrowsize = 1,
            arrowwidth = 2,
            arrowcolor = '#F22E62',
            
    
            ax = 40, ay = -30,
            bordercolor = '#F22E62',
            borderwidth = 2,
            borderpad = 4,
            bgcolor = '#F22E62',
            opacity = 0.8
)

fig.show()
