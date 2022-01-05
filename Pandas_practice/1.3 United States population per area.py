# 전처리
import pandas as pd

pop = pd.read_csv("Data/state-population.csv", encoding = 'utf-8-sig')
area = pd.read_csv("Data/state-areas.csv", encoding = 'utf-8-sig')
abb = pd.read_csv("Data/state-abbrevs.csv", encoding = 'utf-8-sig')

pop = pop.dropna()
cols = pop.columns.to_list()
cols[0] = 'abbreviation'
pop.columns = cols
pop_tot = pop[pop['ages'] == 'total']
pop_18 = pop[pop['ages'] == 'under18']

abb_area = pd.merge(area, abb, on = 'state', how = 'outer')
abb_area = abb_area.fillna("PR")

pop_age_tot_final = pd.merge(pop_tot, abb_area, on = 'abbreviation', how = 'outer').dropna()
pop_age_18_final = pd.merge(pop_18, abb_area, on = 'abbreviation', how = 'outer').dropna()

pop_age_tot_final['pop/area'] = pop_age_tot_final['population'] / pop_age_tot_final['area (sq. mi)']
pop_age_18_final['pop/area'] = pop_age_18_final['population'] / pop_age_18_final['area (sq. mi)']

density_2013_tot = pop_age_tot_final[pop_age_tot_final['year']== 2013]
density_2013_tot = density_2013_tot.sort_values('pop/area', ascending=False)

density_2013_tot = density_2013_tot[['abbreviation', 'pop/area']]
density_2013_tot = density_2013_tot.set_index('abbreviation')
density_2013_tot_top10 = density_2013_tot[:10] 


# iplot 시각화
import chart_studio.plotly as py
import cufflinks as cf
cf.go_offline(connected = True)

layout = {
    'title' : {
        'text' : '<b>Population / Area about total ages in 2013</b>', 
        'font' : {
            'size' : 20
        },
        'x' : 0.5
    },
    
    'xaxis' : {
        'showticklabels' : True,
        'title': {
            'text' : 'Abbreviation',
            'font' : {'size' : 15}
        }
    },

    'yaxis' : {
        'showticklabels' : True,
        'dtick' : 1000,
        'title' : {
            'text' : 'pop/area',
            'font' : {'size' : 15}
        }
    }
}  

density_2013_tot_top10.iplot(kind = 'bar', layout = layout)


# plotly 시각화
import plotly.graph_objects as go
import plotly.offline as pyo
pyo.init_notebook_mode()

import plotly. io as pio
pio.templates

colors = ['#04BFAD',] * len(density_2013_tot_top10)
colors[0] = '#F25C5C'

fig = go.Figure()

fig.add_trace(
    go.Bar(
    x = density_2013_tot_top10.index, y = density_2013_tot_top10['pop/area'],
    marker_color = colors
    )
)

fig.update_layout(
    {
        'title' : {
            'text' : '<b>Population / Area about total ages in 2013</b>',
            'font' : {'size' : 20},
            'x' : 0.5
            },
        
        'xaxis' : {'title' : {'text' : 'Abbreviation'}, 'showticklabels' : True},
        'yaxis' : {'title' : {'text' : 'pop/area'}, 'showticklabels' : True, 'dtick' : 1000},
        
        'template' : 'plotly_white'
    }
)

fig.add_annotation({
    'x' : "DC",
    'y' : 9550,
    
    'text' : 'pop / area in DC',
    'showarrow' : True,
    'font' : {'size' : 10, 'color' : 'white'},
    
    'align' : 'center',
    'arrowhead' : 2,
    'arrowsize' : 1,
    'arrowwidth' : 2,
    'arrowcolor' : '#04BFAD',
    
    'ax' : 20, 'ay' : -50,
    
    'bordercolor' : '#04BFAD',
    'borderwidth' : 2,
    'borderpad' : 7,
    'bgcolor' : '#F25C5C',
    
    'opacity' : 0.9
})
fig.show()
