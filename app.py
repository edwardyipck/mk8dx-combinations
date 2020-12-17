import pandas as pd
import re
import itertools as it

import dash
import dash_table
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Creating the dataframe

drivers = pd.read_csv("assets/data/drivers.csv")
bodies = pd.read_csv("assets/data/bodies.csv")
tires = pd.read_csv("assets/data/tires.csv")
gliders = pd.read_csv("assets/data/gliders.csv")

stats = {"WG": "Weight",
         "AC": "Acceleration",
         "ON": "On-Road traction",
         "OF": "(Off-Road) Traction",
         "MT": "Mini-Turbo",
         "SL": "Ground Speed",
         "SW": "Water Speed",
         "SA": "Anti-Gravity Speed",
         "SG": "Air Speed",
         "TL": "Ground Handling",
         "TW": "Water Handling",
         "TA": "Anti-Gravity Handling",
         "TG": "Air Handling"}

drivers = drivers.rename(columns=stats)
bodies = bodies.rename(columns=stats)
gliders = gliders.rename(columns=stats)
tires = tires.rename(columns=stats)

drivers["Driver"] = drivers["Driver"].apply(lambda x: re.findall('^.*\S', x)[0])
bodies["Body"] = bodies["Body"].apply(lambda x: re.findall('^.*\S', x)[0])
tires["Tire"] = tires["Tire"].apply(lambda x: re.findall('^.*\S', x)[0])
gliders["Glider"] = gliders["Glider"].apply(lambda x: re.findall('^.*\S', x)[0])
tires["Tire"] = tires["Tire"].apply(lambda x : str(x) + " Tires" if "Tires" not in x else x)

namelist = [drivers.Driver.tolist(),bodies.Body.tolist(),tires.Tire.tolist(),gliders.Glider.tolist()]
allnames = list(it.product(*namelist))
statlist = [drivers.drop("Driver",axis=1).values.tolist(),
            bodies.drop("Body",axis=1).values.tolist(),
            tires.drop("Tire",axis=1).values.tolist(),
            gliders.drop("Glider",axis=1).values.tolist()]
allstats = list(it.product(*statlist))
allstats = [[sum(x) for x in zip(i[0],i[1],i[2],i[3])] for i in allstats]
nametable = pd.DataFrame(allnames, columns = ["Driver", "Body", "Tire","Glider"])
stattable = pd.DataFrame(allstats, columns = ['Weight', 'Acceleration', 'On-Road traction', '(Off-Road) Traction',
                                              'Mini-Turbo', 'Ground Speed', 'Water Speed', 'Anti-Gravity Speed',
                                              'Air Speed', 'Ground Handling', 'Water Handling',
                                              'Anti-Gravity Handling', 'Air Handling'])
comb = nametable.join(stattable)
comb["Total"] = comb.sum(axis=1)

# Dash Application

cols = ['Driver', 'Body', 'Tire', 'Glider', 'WG', 'AC', 'ON', 'OF', 'MT', 'SL', 'SW', 'SA', 'SG', 'TL', 'TW', 'TA', 'TG', 'Total']
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

fig = px.scatter(comb.copy()[["Acceleration","Ground Speed"]].drop_duplicates(), x="Acceleration", y="Ground Speed",
                     hover_data=["Acceleration", "Ground Speed"],
                     range_x=[-0.5, 21],range_y=[-0.5, 21])

fig.update_layout(clickmode='event+select')
fig["layout"].pop("updatemenus")
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
fig.update_traces(marker_size=17)


app.layout = html.Div([
    dbc.Row(dbc.Col(html.H3("Mario Kart Combination Selector",style={'margin-top':15}),
                    width={'size': "auto"}),
            justify="center"),
    
    dbc.Row(dbc.Col(html.Div(
        dcc.Markdown('''               
                
           How to use:
                     
           1. Select the categories for the x and y axis of the graph from the dropdowns
           2. Select the slider dropdown, and adjust the slider to your liking
           3. Click on a point on the graph to see the list of combinations in the table on the right
           4. Click the arrows on any column to sort by a specific category, and click on the dot on the left of the table to see your choice in detail
           ''')
        ,style={'margin-left': 80}))),
    
    dbc.Row([
            dbc.Col(html.Div("Select y-axis:",style={'margin-left': 80}),
                    width={'size': 'auto'}
                    ),
             
            dbc.Col(html.Div(
                    dcc.Dropdown(id="slct_y",
                        options=[{"label": i, "value": i} for i in comb.columns][4:-1],
                        multi=False, value="Acceleration",
                        clearable=False)),
                    width={'size': 2}
                    ),
            
            dbc.Col(html.Div("Select x-axis:",style={'margin-left': 80}),
                    width={'size': 'auto'}
                    ),
                        
            dbc.Col(html.Div(
                    dcc.Dropdown(id="slct_x",
                        options=[{"label": i, "value": i} for i in comb.columns][4:-1],
                        multi=False, value="Ground Speed",
                        clearable=False)),
                    width={'size': 2}
                    ),
            
            dbc.Col(html.Div("Select slider:",style={'margin-left': 80}),
                    width={'size': 'auto'}
                    ),
            
            dbc.Col(html.Div(
                    dcc.Dropdown(id="slct_s",
                        options=[{"label": i, "value": i} for i in comb.columns][4:-1],
                        multi=False, value="Mini-Turbo",
                        clearable=False)),
                    width={'size': 2}
                    )
            ]
        ),
    
    dbc.Row(dbc.Col(html.Div(
                    dcc.RangeSlider(
                        id='slider',
                        marks = {i : str(i) for i in range(21)},
                        min=0,
                        max=20,
                        step=1,
                        value=[0,20]),
                        style={'margin-left': 60}),                  
                    width={'size': 10}
                    )
            ),
    
    
    dbc.Row([dbc.Col(html.Div(
                    dcc.Graph(id='graph', figure=fig,style={'width': '70vh', 'height': '70vh'})),
                    width={'size': "auto","offset": -1}),
    
            dbc.Col(html.Div(
                    dbc.Spinner(dash_table.DataTable(id="table",
                    columns=[{"id": i, "name": j} for i,j  in zip(comb.reset_index().columns[1:],cols)],
                    tooltip_header={i: i for i in comb.reset_index().columns[1:]},
                    data=[], sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    row_selectable="single",
                    selected_rows=[],
                    page_current=0,
                    style_table={'height': 500, 'overflowY': 'scroll', 'overflowX': 'scroll','width': 800},
                    style_data={'whiteSpace': 'normal', 'height': 'auto',},
                    style_cell={'textAlign': 'left'},
                    tooltip_delay=0,
                    tooltip_duration=None,))
    
    ),width={'size': "auto"},align="center")]),
    
    html.Div([
        html.Pre(id='click-data'),
    ]),
    
    dbc.Row([dbc.Col([
    html.Img(id = 'image_1', width=128, height=128,src=app.get_asset_url("blank.png"),style={'margin-left': 65}),
    html.Img(id = 'image_2', width=120, height=77,src=app.get_asset_url("blank.png")),
    html.Img(id = 'image_3', width=120, height=77,src=app.get_asset_url("blank.png")),
    html.Img(id = 'image_4', width=120, height=77,src=app.get_asset_url("blank.png"))],width={'size': 'auto'}),
            dbc.Col(html.Div(dcc.Graph(id='graph2', figure={})),width={'size': "auto"},align="start")]
    )
    
])

@app.callback(
    Output('table', 'data'),
    Output('table', 'page_current'),
    Output('table', 'derived_virtual_selected_rows'),
    Input('graph', 'clickData'),
    Input('slct_y', 'value'),
    Input('slct_x', 'value'),
    Input('slct_s', 'value'),
    Input('slider', 'value'),
    Input('table', 'sort_by'))
    
def update_table(clickData,ycol,xcol,scol,sval,sortby):

    if all(i != None for i in [clickData,ycol,xcol,scol]) and len(set([ycol,xcol,scol])) ==3:
        yval = int(clickData['points'][0]['y'])
        xval = int(clickData['points'][0]['x'])
        data = comb[(comb[ycol] == yval) & (comb[xcol] == xval) & (comb[scol].between(sval[0],sval[1]))]
        if len(sortby):
            for i in sortby:
                data = data.sort_values([col['column_id'] for col in sortby],
                        ascending=[col['direction'] == 'asc'for col in sortby],inplace=False)
                                        
            return data.to_dict("records"), 0, [0]
        
        return data.to_dict("records"), 0, [0]     
    else:
        return [], 0, [0]
    
@app.callback(
    Output('graph', 'figure'),
    Input('slct_y', 'value'),
    Input('slct_x', 'value'),
    Input('slct_s', 'value'),
    Input('slider', 'value'))

def update_graph(ycol,xcol,scol,sval):
    if all(i != None for i in [ycol,xcol,scol]) and len(set([ycol,xcol,scol])) ==3:
        data = comb.copy()[[ycol,xcol,scol]].drop_duplicates()
        data = data[data[scol].between(sval[0],sval[1])]
        fig = px.scatter(data, x=xcol, y=ycol,color = scol, range_color=[0,20],
                         hover_data=[ycol, xcol,scol],
                         range_x=[-0.5, 21],range_y=[-0.5, 21])
        fig.update_layout(clickmode='event+select',
                          hoverlabel=dict(bgcolor="#181A1B", font_color='white'))

        fig["layout"].pop("updatemenus")
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        fig.update_traces(marker_size=17)
        return fig
    else:
        return {}
    
@app.callback(
    Output('image_1','src'),
    Output('image_2','src'),
    Output('image_3','src'),
    Output('image_4','src'),
    Output('graph2', 'figure'),
    Input('table', 'derived_virtual_data'),
    Input('table', 'derived_virtual_selected_rows'))
    
def select(data,select):
    if data != [] and select !=[] and data != None and select !=None:
        driver = str(data[select[0]]['Driver']).replace(" ","_").lower()
        body = str(data[select[0]]['Body']).replace(" ","_").lower()
        tires = str(data[select[0]]['Tire']).replace(" ","_").lower()
        glider = str(data[select[0]]['Glider']).replace(" ","_").lower()
        
        fig = px.bar(
            x=list(data[select[0]].values())[4:-1][::-1],
            y=list(comb.columns[4:-1])[::-1],
            text=list(data[select[0]].values())[4:-1][::-1],
            range_x=[0, 21],
            orientation='h',
            color=px.colors.qualitative.Dark24[:13])
        
        fig["layout"].pop("updatemenus")
        fig.update_layout(showlegend = False)
        fig.update_layout(hoverlabel=dict(bgcolor="#181A1B", font_color='white'))
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        
        return (app.get_asset_url('driver/'+driver+'.png'), app.get_asset_url('body/'+body+'.png'), app.get_asset_url('tires/'+tires+'.png'), app.get_asset_url('glider/'+glider+'.png'),fig)
    else:
        return (app.get_asset_url("blank.png"),app.get_asset_url("blank.png"),app.get_asset_url("blank.png"),app.get_asset_url("blank.png"),{})     
                
@app.callback(
    [Output("progress", "value"), Output("progress", "children")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):

    progress = min(n % 110, 100)
    return progress, f"{progress} %" if progress >= 5 else ""                
    
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run_server(debug=False)
