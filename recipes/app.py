### Quick description:
# Dash practice with recipes from the Allrecipes project
# 
# Follow-on work from the tutorial from realpython.com\
# https://www.justintodata.com/python-interactive-dashboard-with-plotly-dash-tutorial/
# 
# Ideas / Plan:
# - [x] Make sugar column into number
# - [x] Plot average review vs amount of sugar
# - [X] Interactivity: can choose y (avg_rating or no_ratings) and x (sugar content or calories)




###
# The following code is a good starting point for heroku apps,
# as it contains heroku-specific parts (instead of jupyter-specific parts):

import dash
from dash import dcc
from dash import html
#from jupyter_dash import JupyterDash 
import pandas as pd
import plotly.express as px

import numpy as np
from dash.dependencies import Output, Input

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Recipes: is it sugar or calories?"

###
# Paste code here related to obtaining data
# (This section is the same for heroku & jupyter)

# # Dash practice with recipes from the Allrecipes project
# 
# Follow-on work from the tutorial from realpython.com\
# https://www.justintodata.com/python-interactive-dashboard-with-plotly-dash-tutorial/
# 
# Ideas / Plan:
# - [x] Make sugar column into number
# - [x] Plot average review vs amount of sugar
# - [x] Interactivity: can choose y (avg_rating or no_ratings) and x (sugar content or calories)

# # Part 0: prep data

# ### Import libraries

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# read in data
data = pd.read_csv("processed_recipe_data.csv")


# In[3]:


data.head(1)


# In[4]:


data.info()


# In[5]:


# turn relevant numeric columns into numbers
data['nutrition.sugarContent.g'] = data['nutrition.sugarContent'].str.replace(r' g', '').astype(float)
data['nutrition.calories.kcal'] = data['nutrition.calories'].str.replace(r' calories', '').astype(float)


# In[6]:


# check
data[['nutrition.sugarContent', 'nutrition.sugarContent.g']].head(3)


# In[7]:


# check
data[['nutrition.calories', 'nutrition.calories.kcal']].head(3)


# In[8]:


# select only the relevant columns
data = data.iloc[:, [0, 1, 2, 4, 5, 36, 35]]


# In[9]:


# inspect
data.shape


# In[10]:


# drop rows that have any null values
data.dropna(axis=0, how='any', inplace=True)


# In[11]:


# inspect
data.shape


# In[12]:


data.columns.tolist()


###
# Paste code here related to designing & running the app
# (This section is the same for heroku & jupyter):


# ### Interactivity with callbacks<br>(a tweaked version of the script)
# 
# Interactive filters:
# - Rating metric
# - Nutrition parameter


app.layout = html.Div(
    children=[
        
        # header
        html.Div(
            children=[
                html.Img(
                    src=r'assets/apple_pie_logo.jpg', alt='image', className="header-emoji", height="125"),
                html.H1(
                    children="Recipe explorations", className="header-title"),
                html.P(
                    children=["Analyse the behavior of recipe ratings on allrecipes.com", html.Br(), "based on their nutritional values"],
                    className="header-description")],
            className="header"),

        # inputs (dropdown menus)
        html.Div(
            children=[
                             
                
                # dropdown menu to choose ratings parameter
                html.Div(
                    children=[
                        html.Div(children="Rating parameter", className="menu-title"),
                        
                        dcc.Dropdown(
                            options=[
                                {"label": nice_name, "value": col_name}
                                for (nice_name, col_name) in [('Average rating', 'avg_rating'), ('Number of ratings', 'ratings_no')]],
                            value = 'avg_rating', # default value
                            id='rating-filter',
                            clearable=False,
                            className="dropdown")]),
                
                
                # dropdown menu to choose nutrition parameter
                html.Div(
                    children=[
                        html.Div(children="Nutrition parameter", className="menu-title"),
                        
                        dcc.Dropdown(
                            options=[
                                {"label": nice_name, "value": col_name}
                                for (nice_name, col_name) in [('Calories', 'nutrition.calories.kcal'), ('Sugar content', 'nutrition.sugarContent.g')]],
                            value = 'nutrition.calories.kcal', # default value
                            id='nutrient-filter',
                            clearable=False,
                            className="dropdown")]),
            ],
            className="menu",
        ),
        
        # graph
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="recipe-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


# In[18]:


@app.callback(
    Output("recipe-chart", "figure"),
    [
        Input("nutrient-filter", "value"),
        Input("rating-filter", "value")
    ],
)


def update_charts(nutrient_choice, rating_choice):
    
    # data range
    filtered_data = data[[nutrient_choice, rating_choice]]

    
    # chart text (chart title, axes titles, hover over text)    
    if nutrient_choice == 'nutrition.calories.kcal':
        x_axis_title = 'Calories per serving (kcal)'
        x_hover = 'calories'
        hov_text_x = '%{x:.0f} calories<extra></extra>'
    elif nutrient_choice == 'nutrition.sugarContent.g':
        x_axis_title = 'Sugar content per serving (grams)'
        hov_text_x = '%{x:.0f} g sugar<extra></extra>'
    
    
    if rating_choice == 'avg_rating':
        chart_title = 'How many stars?'
        y_axis_title = 'Average rating'
        hov_text_y = '%{y:.1f} stars for '
    elif rating_choice == 'ratings_no':
        chart_title = 'How many ratings?'
        y_axis_title = 'Number of ratings'
        hov_text_y = '%{y:.0f} total ratings for '
        
       # '%{y:.1f} %{customdata} for %{x:.1f} %{customdata[1]}<extra></extra>'

    # update figure
    fig = px.scatter(filtered_data,
                     x=nutrient_choice,
                     y=rating_choice)

    fig.update_traces(marker=dict(symbol='circle',
                                  color='rgba(235, 195, 35, 0.25)',
                                  line=dict(width=0.25)),
                      hovertemplate = hov_text_y + hov_text_x)

    fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor='#E1E5EA',
                     zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig.update_yaxes(showgrid=True, gridwidth=0.05, gridcolor='#E1E5EA',
                     zeroline=True, zerolinewidth=1, zerolinecolor='Black')

    fig.update_layout(title=dict(text=chart_title,
                                            x=0.05,
                                            xanchor='left'),
                                 xaxis=dict(fixedrange=True,
                                            title=x_axis_title),
                                 yaxis=dict(fixedrange=True,
                                            title=y_axis_title),
                                 #paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)')

    
    return fig


###
# Deploy to heroku

if __name__ == "__main__":
    app.run_server(debug=True)
