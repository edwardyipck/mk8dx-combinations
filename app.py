import dash
import dash_table
import plotly.express as px
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import dataframe

comb, driver_list = dataframe.dataframe()
cols = ['Driver', 'Body', 'Tires', 'Glider', 'WG', 'AC', 'ON', 'OF', 'MT', 'SL', 'SW', 'SA', 'SG', 'TL', 'TW', 'TA', 'TG', 'Total']
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

fig = px.scatter(comb[["Acceleration","Ground Speed"]].drop_duplicates(), x="Acceleration", y="Ground Speed",
                     hover_data=["Acceleration", "Ground Speed"],
                     range_x=[-0.5, 21],range_y=[-0.5, 21])

fig.update_layout(clickmode='event+select')
fig["layout"].pop("updatemenus")
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
fig.update_traces(marker_size=17)


app.layout = html.Div([
    dbc.Row(dbc.Col(html.H3("Mario Kart 8 Deluxe Combination Selector",style={'margin-top':15}),
                    width={'size': "auto"}),
            justify="center"),
    
    dbc.Row(dbc.Col(html.Div(
        dcc.Markdown('''               
           This application uses data from **Mario Kart 8 Deluxe** to create an interactive graphs, note that the total sum of a particular stat maxes out at 20.
                     
           How to use:
           
           1. Select the driver you want on the dropdown, you can select multiple drivers. Leave it empty to select all drivers.
           2. Select the categories for the x and y axis of the graph from the dropdowns
           3. Select the category for the slider dropdown, and adjust the slider to your liking
           4. Click on a point on the graph to see the list of combinations in the table on the right
           5. Click the arrows on any column to sort by a specific category, and click on the dot on the left of the table to see your choice in detail
           ''')
        ,style={'margin-left': 80}))),
    
    dbc.Row([dbc.Col(html.Div("Select driver:",style={'margin-left': 80}),
                    width={'size': 'auto'}
                    ),
             
            dbc.Col(html.Div(
                    dcc.Dropdown(id="slct_driver",
                        options=[{"label": i, "value": i} for i in driver_list],
                        multi=True,
                        clearable=False,
                        placeholder="All Drivers",),
                        style={"width": "250px",'margin-left': -20}),
                    width={'size': "auto"}
                    ),
            
            dbc.Col(html.Div("Select y-axis:",style={'margin-left': -10}),
                    width={'size': 'auto'}
                    ),
             
            dbc.Col(html.Div(
                    dcc.Dropdown(id="slct_y",
                        options=[{"label": i, "value": i} for i in comb.columns][4:-1],
                        multi=False, value="Acceleration",
                        clearable=False),
                        style={"width": "200px",'margin-left': -20}),
                    width={'size': "auto"}
                    ),
            
            dbc.Col(html.Div("Select x-axis:",style={'margin-left': -10}),
                    width={'size': 'auto'}
                    ),
                        
            dbc.Col(html.Div(
                    dcc.Dropdown(id="slct_x",
                        options=[{"label": i, "value": i} for i in comb.columns][4:-1],
                        multi=False, value="Ground Speed",
                        clearable=False),
                        style={"width": "200px",'margin-left': -20}),
                    width={'size': "auto"}
                    ),
            
            dbc.Col(html.Div("Select slider:",style={'margin-left': -10}),
                    width={'size': 'auto'}
                    ),
            
            dbc.Col(html.Div(
                    dcc.Dropdown(id="slct_s",
                        options=[{"label": i, "value": i} for i in comb.columns][4:-1],
                        multi=False, value="Mini-Turbo",
                        clearable=False),
                        style={"width": "200px",'margin-left': -20}),
                    width={'size': "auto"}
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
    
            dbc.Col(dbc.Spinner(html.Div(
                    dash_table.DataTable(id="table",
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
    
    dbc.Row([dbc.Col(dbc.Spinner([
    html.Img(id = 'image_1', width=128, height=128,src=app.get_asset_url("blank.png"),style={'margin-left': 65}),
    html.Img(id = 'image_2', width=120, height=77,src=app.get_asset_url("blank.png")),
    html.Img(id = 'image_3', width=120, height=77,src=app.get_asset_url("blank.png")),
    html.Img(id = 'image_4', width=120, height=77,src=app.get_asset_url("blank.png"))]),width={'size': 5}),
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
    Input('slct_driver', 'value'),
    Input('table', 'sort_by'))
    
def update_table(clickData,ycol,xcol,scol,sval,driver,sortby):

    if all(i != None for i in [clickData,ycol,xcol,scol]) and len(set([ycol,xcol,scol])) ==3:
        yval = int(clickData['points'][0]['y'])
        xval = int(clickData['points'][0]['x'])
        data = comb[(comb[ycol] == yval) & (comb[xcol] == xval) & (comb[scol].between(sval[0],sval[1]))]
        if driver!=None and driver != []:
            data=data[data["Driver"].isin(driver)]
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
    Output('graph', 'clickData'),
    Input('slct_y', 'value'),
    Input('slct_x', 'value'),
    Input('slct_s', 'value'),
    Input('slider', 'value'),
    Input('slct_driver', 'value'))

def update_graph(ycol,xcol,scol,sval,driver):
    if all(i != None for i in [ycol,xcol,scol]) and len(set([ycol,xcol,scol])) ==3:
        if driver!=None and driver != []:
            data=comb[comb["Driver"].isin(driver)]
        else:
            data=comb
        data = data[[ycol,xcol,scol]].drop_duplicates()
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
        return fig, None
    else:
        return {}, None
    
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
        tires = str(data[select[0]]['Tires']).replace(" ","_").lower()
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

        return (app.get_asset_url('driver/%s.png' % driver), app.get_asset_url('body/%s.png' % body), app.get_asset_url('tires/%s.png' % tires), app.get_asset_url('glider/%s.png' % glider),fig)
    else:
        return (app.get_asset_url("blank.png"),app.get_asset_url("blank.png"),app.get_asset_url("blank.png"),app.get_asset_url("blank.png"),{})          

if __name__ == '__main__':
    app.run_server(debug=False)
