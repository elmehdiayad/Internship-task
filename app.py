

########################################################################################################################

#El Mehdi AYAD proposal for Software Development internship task


#in this application I used dash Cytoscape which is is a graph visualization component for creating easily 
#customizable, high-performance, interactive, and web-based networks. It extends and renders Cytoscape.js, 
#and offers deep integration with Dash layouts and callbacks, enabling the creation of powerful networks in
# conjunction with the rich collection of Dash components as well as established computational biology and 
# network science libraries such as Biopython and network X.

#Make sure that dash and its dependent libraries are correctly installed:

# pip install dash dash-html-components
#If you want to install the latest versions, check out the Dash docs on installation.

#Usage
#Install the library using pip:

# pip install dash-cytoscape
########################################################################################################################
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#creating the nodes
nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20*lat, 'y': -20*long}
    }
    for short, label, long, lat in (
        ('1', '1', 34.03, -118.25),
        ('2', '2', 49.28, -123.12),
        ('3', '3', 41.88, -87.63),

    )
]
#creating the edges
edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('1', '2'),
        ('1', '3'),
    )
]
#elemnts : the graph
elements = nodes + edges


markdown_text = 'Node Selected: '

#creating the default stylesheet
default_stylesheet = [
    {
      'selector': 'node',
          'style': {
              'background-color': '#BFD7B5',
              'label': 'data(label)'
          }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    }
]


#now we create the app layout it contains the html elements
app.layout = html.Div([
    html.Div(style={'vertical-align': 'middle'}, children=[

        dcc.Markdown(id='cytoscape-selectedNodeData-markdown'),

        html.Div(style={'width': '50%', 'display': 'inline'}, children=[
            'Node Color:',
            dcc.Input(id='input-bg-color', type='text', placeholder= 'Select a Node')
        ]),
        html.Div(style={'width': '50%', 'display': 'inline'}, children=[
            'Node Width:',
            dcc.Input(id='input-width', type='text', placeholder= 'Select a Node')
        ]),
        html.Div(style={'width': '50%', 'display': 'inline'}, children=[
            'Node Height:',
            dcc.Input(id='input-height', type='text', placeholder= 'Select a Node')
        ]),
    ]),


    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'circle'},
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '450px'},
        elements=elements
    )
])

#the primary callback, it takes the taped node, the values form the stylesheet, and returns the updated one
@app.callback([Output('cytoscape', 'stylesheet'),
               Output('cytoscape-selectedNodeData-markdown', 'children'),
               Output(component_id='input-bg-color', component_property='placeholder'),
               Output(component_id='input-width', component_property='placeholder'),
               Output(component_id='input-height', component_property='placeholder')],
              [Input('cytoscape', 'tapNode'),
               Input('input-bg-color', 'value'),
               Input('input-width', 'value'),
               Input('input-height', 'value')])

def update_node(node, bg_color, width, height):
    if not node:
        return default_stylesheet, '', '', '', ''
    
    if bg_color is None:
        bg_color = ''
    
    if width is None:
        width = ''

    if height is None:
          height = ''

    #now we modify the default stylesheets adding the user preferences
    default_stylesheet.append(
        {
            'selector': 'node[id = "{}"]'.format(node['data']['id']),
            'style': {
                'background-color': bg_color,
                'width' : width,
                'height' : height
            }
        }
    )
    return  default_stylesheet, markdown_text + node['data']['label'], node['style']['background-color'], node['style']['width'], node['style']['height']


#this callback is used to show the node values when the user click on a node
@app.callback([Output(component_id='input-bg-color', component_property='value'),
               Output(component_id='input-width', component_property='value'),
               Output(component_id='input-height', component_property='value')],
              [Input('cytoscape', 'tapNode')])
def update(node):
  if node:
    return  node['style']['background-color'], node['style']['width'], node['style']['height'],

  return '', '', ''

if __name__ == '__main__':
    app.run_server(debug=True)