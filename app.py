import dask.dataframe as dd
import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go


# For map
import datashader as ds
import datashader.transfer_functions as tf

#'spc_common'
#'borough'



# external JavaScript files
external_scripts = [
    {
        'src': 'https://www.googletagmanager.com/gtag/js?id=G-ET46TBPVET',
    }
]


# app initialize
dash_app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],

)


app = dash_app.server
dash_app.config["suppress_callback_exceptions"] = True
dash_app.title = 'NYC Tree Health 2015'
dash_app._favicon = ('assets/favicon.ico')


# Load data
# You can download the data here: https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh
# The csv was not uploaded to Github because of file constraints, but you can compress it.
data = dd.read_csv('assets/2015_Street_Tree_Census_-_Tree_Data.csv.gz', blocksize = None)
data = data.dropna(subset=['health', 'steward'])


# Clean data
data['spc_common'] = data['spc_common'].fillna('Not Available')
data['spc_common'] = data['spc_common'].str.replace("'Schubert' chokecherry", 'Schubert chokecherry')
data['spc_common'] = data['spc_common'].str.title()
data['spc_common'] = data['spc_common'].str.replace("'S", "'s")



df = data[['tree_id', 'health', 'spc_common', 'steward', 'borough', 'latitude', 'longitude', 'x_sp', 'y_sp']]
df = df.compute()


spc = df['spc_common'].unique().tolist()
spc.sort()
boro = df['borough'].unique().tolist()



# Steward: 'None' '1or2' '3or4' '4orMore'
# Health: 'Fair' 'Good' 'Poor' 
df['health'] = df['health'].astype('category')



# Color Key
color_key = {
   'Poor': 'red',
   'Fair': 'orange',
   'Good': 'green'
}

# Steward Key
steward_key = {
    0: 'None',
    1: '1or2',
    2: '3or4',
    3: '4orMore'
    }

# Mapbox API Key
# Stored in another file. Please obtain your own key from mapbox.com
key_file = open('assets/api.key')
lines = key_file.readlines()
mapbox_api = lines[0].rstrip()





def build_banner():
   return html.Div(
      id="banner",
      className="banner",
      children=[
        html.Img(src=dash_app.get_asset_url("cunysps_2021_2linelogo_spsblue_1.png"), style={'height':'75%', 'width':'75%'}),
        html.H6("NYC Boroughs and Tree Heath 2015"),
        ],
    )

def build_graph_title(title):
   return html.P(className="graph-title", children=title)


dash_app.layout = html.Div(
  children=[
    html.Div(
        id="top-row",
        children=[
            html.Div(
               className="row",
               id="top-row-header",
               children=[
                  html.Div(
                     className="column",
                     id="header-container",
                     children=[
                         build_banner(),
                         html.P(
                            id="instructions",
                            children=[
                                "This Dash app utilizes data from ",
                                html.A(
                                    "NYC's 2015 Street Tree Census",
                                    href='https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh'
                                    ),
                                ". This is designed for an arborist studying the health of various tree species across each borough.",
                                " The app displays information about the health of the trees based upon borough and steward activity. ",
                                "The graphs will dynamically update based upon the species, borough, and stewards selected.",
                                html.Br(),
                                html.Br(),
                                "This app is hosted on ",
                                html.A(
                                    "Azure's cloud platform (https://portal.azure.com)",
                                    href='https://portal.azure.com'
                                    ),
                                ". The Github for this application is here ",
                                html.A(
                                    "https://github.com/logicalschema/data608-treehealth-dash-sslee",
                                    href='https://github.com/logicalschema/data608-treehealth-dash-sslee'
                                    ),
                                ".",
                                html.Br(),
                                html.Br(),
                            ],
                         ),
                         build_graph_title(html.B("Species")),
                         dcc.Dropdown(
                           id="spc-dropdown",
                           options=[
                               {"label": i, "value": i} for i in spc
                           ],
                           multi=True,
                           value=[spc[0], spc[1], spc[52]],
                           ),
                         build_graph_title(html.B("Borough(s)")),
                         dcc.Dropdown(
                           id="borough-dropdown",
                           options=[
                               {"label": i, "value": i} for i in boro
                           ],
                           multi=True,
                           value=[boro[0], boro[1], boro[2], boro[3], boro[4]]
                           ),
                         build_graph_title(html.B("Steward(s)")),
                         dcc.Slider(
                           id="steward-slider",
                           min=0,
                           max=3,
                           step=None,
                           marks={
                               # 'None' '1or2' '3or4' '4orMore'
                               0: 'None',
                               1: '1 or 2',
                               2: '3 or 4',
                               3: '4 or More'
                           },
                           value=3
                           )

                   ]
                  ),
                  html.Div(
                     className="column",
                     id="top-row-graphs",
                     children=[

                          dcc.Loading(
                            html.Div(
                              id="map",
                              className="row",
                              children=[
                              # dcc Graph here
                                 dcc.Graph(id='map-graph')
                              ]

                            )
                          )
                     ]
                  ),
               ]
            ),
          ]
    ),
    html.Div(
      id="bottom-row",
      children=[
          html.Div(
              className="bottom-row",
              id="bottom-row-header",
              children=[
                  html.Div(
                     className="column",
                     id="form-bar-container",
                     children=[
                         build_graph_title("Tree Health and Stewardship"),
                         dcc.Graph(id='form-bar-graph'),
                     ]
                  ),
                  html.Div(
                     className="column",
                     id="form-text-container",
                     children=[
                         html.P(
                            id="lower-text-box"                         ),
                     ],
                  ),
              ]
              )
      ]
      ),
])


# Update bar plot
@dash_app.callback(
    Output("form-bar-graph", "figure"),
    [
        Input("spc-dropdown", "value"),
        Input("borough-dropdown", "value"),
        Input("steward-slider", "value"),
    ],
)
def update_bar(spc_dropdow_name, borough_dropdown, steward_slider):
   # Note: Steward: 0: 'None' 1: '1or2' 2: '3or4' 3: '4orMore'
   # Select the specific data based upon borough and species
   dff = df[df["spc_common"].isin(spc_dropdow_name) & df["borough"].isin(borough_dropdown)]


   # Select the trees with steward values
   steward_values = []
   for i in range(0, steward_slider + 1):
      steward_values.append(steward_key[i])

   dff = dff[dff["steward"].isin(steward_values)]


   grouped_df = dff.groupby(['steward', 'health']).size().reset_index(name="count")

   fig = px.bar(
     grouped_df, 
     x="steward", 
     y="count", 
     color="health", 
     color_discrete_map=color_key, 
     category_orders={"health": ["Poor", "Fair", "Good"]},
     title="Trees Organized by Health and Stewardship"
   )

   fig.update_layout(
     plot_bgcolor="rgba(0, 0, 0, 0)",
     yaxis_type="log", 
     barmode='group'
    )


   return fig



# Update map
@dash_app.callback(
    Output("map-graph", "figure"),
    [
        Input("spc-dropdown", "value"),
        Input("borough-dropdown", "value"),
        Input("steward-slider", "value"),
    ],
)
def update_map(spc_dropdow_name, borough_dropdown, steward_slider):
    # Note: Steward: 0: 'None' 1: '1or2' 2: '3or4' 3: '4orMore'
    # Select the specific data based upon borough and species
    dff = df[df["spc_common"].isin(spc_dropdow_name) & df["borough"].isin(borough_dropdown)]

    # Select the trees with steward values
    steward_values = []
    for i in range(0, steward_slider + 1):
        steward_values.append(steward_key[i])

    dff = dff[dff["steward"].isin(steward_values)]


    cvs = ds.Canvas(800, 800)
    aggs = cvs.points(dff, x='longitude', y='latitude', agg=ds.count_cat('health'))
    coords_lat, coords_lon = aggs.coords['latitude'].values, aggs.coords['longitude'].values

    coordinates = [[coords_lon[0], coords_lat[0]],
                  [coords_lon[-1], coords_lat[0]],
                  [coords_lon[-1], coords_lat[-1]],
                  [coords_lon[0], coords_lat[-1]]]

    center = {'lat':40.70229736498986, 'lon':-74.01581689028704}

    img = tf.shade(aggs, color_key=color_key, how='eq_hist')[::-1].to_pil()
    fig = px.scatter_mapbox(dff[:1], lat='latitude', lon='longitude', center = center, zoom=10)

    fig.update_layout(mapbox_style="light",
                      mapbox_accesstoken=mapbox_api,
                      mapbox_layers=[
                          {
                        "sourcetype": "image",
                        "source": img,
                        "coordinates": coordinates
                          }
                      ],
                      width=800,
                      height=800
    )

    return fig



# Update bar plot
@dash_app.callback(
    Output("lower-text-box", "children"),
    [
        Input("spc-dropdown", "value"),
        Input("borough-dropdown", "value"),
        Input("steward-slider", "value"),
    ],
)
def update_textbox(spc_dropdow_name, borough_dropdown, steward_slider):
   # Note: Steward: 0: 'None' 1: '1or2' 2: '3or4' 3: '4orMore'
   # Select the specific data based upon borough and species
   dff = df[df["spc_common"].isin(spc_dropdow_name) & df["borough"].isin(borough_dropdown)]

   # Select the trees with steward values
   steward_values = []
   for i in range(0, steward_slider + 1):
     steward_values.append(steward_key[i])

   dff = dff[dff["steward"].isin(steward_values)]


   value_counts = dff['health'].value_counts(normalize=True)
   values = value_counts.index.tolist()
   counts = value_counts.tolist()
   z = list(zip(values, counts))

   strText = ""
   lines = []
   for i in z:
      strText = str(i[0]) + ' : {:.2f}'.format(i[1] * 100) + "%"
      lines.append(strText)
      lines.append(html.Br())


   children = [
     html.B('Information:'),
     html.P('Species: {}'.format(spc_dropdow_name)),
     html.P('Borough: {}'.format(borough_dropdown)),
     html.P('Steward Values Up to: {}'.format(steward_key[steward_slider])),
     html.P([html.Br(), html.B('Proportions for Tree Health')]),
     html.P(lines)
   ]

   return children




# Running the server
if __name__ == "__main__":
    dash_app.run_server(debug=True)