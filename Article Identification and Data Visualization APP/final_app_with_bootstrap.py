import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import dash_table
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from newsplease import NewsPlease
import pickle
from keras.preprocessing.text import text_to_word_sequence
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


stopw = set(stopwords.words('english'))
snow = nltk.stem.SnowballStemmer('english')
# lets remove words like not, very from stop words as they are meaninging in the reviews
reqd_words = set(['only','very',"doesn't",'few','not'])
stopw = stopw - reqd_words


def clean_text(article):

  cleaned_article = []
  cleaned_words_list = text_to_word_sequence(article)
  for word in cleaned_words_list:
    if word not in stopw and len(word) > 2:
      cleaned_article.append(snow.stem(word))
  return ' '.join(cleaned_article)


def recommend_policies(article_text):
  if len(article_text):
      article = article_text
      policies_recommended = []
      # policy_text_arrays = policy_df['policy_text'].values
      policy_text_arrays = policy_df['cleaned_policy_texts'].values
      article_index = len(policy_text_arrays)
      policy_text_arrays = np.append(policy_text_arrays, article)
      tfidf = TfidfVectorizer(ngram_range=(1,2))
      tfidf_matrix = tfidf.fit_transform(policy_text_arrays)
      cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
      #print("cosine_similarity matrix is :")
      #print(cosine_similarities)
      cosine_values_series = pd.Series(cosine_similarities[article_index]).sort_values(ascending=False)
      #print(cosine_values_series)
      top_10_indexes = list(cosine_values_series.iloc[1:6].index)
      #print(f'top 10 indexes are {top_10_indexes}')
      for i in top_10_indexes:
        #policies_recommended.append((policy_df['policy_name'][i], cosine_values_series[i]))
        policies_recommended.append(policy_df['policy_name'][i])

      # recomend_df = pd.DataFrame(policies_recommended[:5], columns=['policy_names in order', 'cosine similarity'])

      #return recomend_df.to_dict('records')
      cos_val_list = list(cosine_values_series[1:6])
      df = pd.DataFrame({'Recommended policies':policies_recommended, 'cosine similarity values':cos_val_list})
      return df


tfidf_uni_loaded = pickle.load(open('tfidf_uni_pickle_vectorizer.sav', 'rb'))
tfidf_uni_model = pickle.load(open('log_tfidf_uni_model.sav', 'rb'))




token = "pk.eyJ1Ijoia2FsaTYiLCJhIjoiY2swejc4ZXQzMDZzdTNrbzV1eXpwejhzeiJ9.Xw7BdlQY-wbll9qirrcnuw"


app = dash.Dash(__name__)
#reading the dataframe
#df_01 = pd.read_csv("data/final_admin_mapped_data.csv", dtype={'Actor1Religion2Code':str,
# 'Actor1Type3Code':str,
# 'Actor2KnownGroupCode':str,
#'Actor2Religion2Code':str,
# 'Actor2Type3Code':str,
# 'Actor2Geo_ADM2Code':str})


df_01 = pd.read_csv("data/final_admin_mapped_selected.csv")

#df_01 = df_01[['Year', 'Actor1Type1CodeName', 'ActionGeo_Lat', 'ActionGeo_Long', 'admin1_fipsnames', 'Actor1Name','SOURCEURL']].drop_duplicates()
policy_df = pd.read_csv('data/policy_df.csv')



app_colors = {
        'background': '#0C0F0A',
        'text': '#FFFFFF'
}
#app = dash.Dash(__name__,external_stylesheets=external_stylesheets)


#app = dash.Dash(__name__, assets_external_path="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")
#app.scripts.config.serve_locally = False
app.title = 'GDELT DATA OMDENA'
#app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'})

year_options = []
for y in df_01['Year'].unique():
    year_options.append({'label':str(y), 'value':y})

# option for admin1 Dropdown
admin_options = []
for a in df_01['admin1_fipsnames'].unique():
    admin_options.append({'label':a, 'value':a})

def gen_map(filtered_df):
    traces = []
    for religion in filtered_df['Actor1Type1CodeName'].unique():
        df_religion_level = filtered_df[filtered_df['Actor1Type1CodeName'].isin([religion])]

        traces.append(go.Scattermapbox(
        lat=df_religion_level['ActionGeo_Lat'],
        lon=df_religion_level['ActionGeo_Long'],
        mode='markers',
        name=religion,
        text=df_religion_level['Actor1Name'],
        opacity=1))

    return {'data': traces,
    'layout': {'mapbox': {'accesstoken': (token),'center':go.layout.mapbox.Center(lat=20.5, lon=78.9),
                          'zoom':3, "style":'dark'},
              'autosize':True, 'height':400, 'margin':dict(l=0,r=5,b=0,t=5),
              "paper_bgcolor":app_colors['background']
    }}


def update_rec_table(df):
    #print(df.head())
    value_header = ['policies recommended', 'cosine similariites']
    value_cell = [df['Recommended policies'], df['cosine similarity values']]
    trace = go.Table(
    header={"values": value_header, "fill": {"color": "#8B7CC8"}, "height": 35,
            "line": {"width": 2, "color": "#685000"}, "font": {"size": 18, "color":app_colors['text']}},
    cells={"values": value_cell, "fill": {"color": app_colors['background']},
            "font": {"size": 15, "color":app_colors['text']}
            }
    )
    layout = go.Layout(title=f"Entry Draft", height=600)
    return [html.Div(dcc.Graph({"data": trace, "layout": layout})
    )]
    #fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
    #                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
    #                     ])

    return fig


def generate_table(df, max_rows=10):
    #print(df.head())
    return html.Table(className="responsive-table",
                      children=[
                          html.Thead(
                              html.Tr(
                                  children=[
                                      html.Th(col.title()) for col in df.columns.values],
                                  style={'color':app_colors['text']}
                                  )
                              ),
                          html.Tbody(
                              [

                              html.Tr(
                                  children=[
                                      html.Td(data) for data in d
                                      ], style={'color':app_colors['text'],
                                                'background-color':app_colors['background']}
                                  )
                               for d in df.values.tolist()])
                          ]
    )




app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='year_drop_id',
                options=year_options,
                searchable=False,#value=df_01['Year'].min(),
                placeholder="Select a Year",
                multi=True,
                value = [2008],
                style={'backgroundColor': app_colors['background'],
                       'position': 'relative'}
            )
        ],
        className='col-sm'),

        html.Div(
        [
            dcc.Dropdown(
                id='admin1_drop_id',
                options=admin_options,
                searchable=False, #value=admin_options[0],
                placeholder="Select admin Level",
                multi=True,
                value=df_01['admin1_fipsnames'].unique()[0],
                style={'backgroundColor': app_colors['background'],
                'position': 'relative'}
            )
        ], className='col-sm')
    ], className='row', style={'margin-bottom':'10px'}),
    # Map and Table
    html.Div(className='container-fluid', children = [
            dcc.Graph(id='map_id')
            ], style={'margin-top': 0, "padding-top": "0px"}),

    html.Div(className='col-sm', children=[
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df_01.columns],
        data=df_01.to_dict('records'),
        row_selectable='single',
        selected_rows = [],
        fixed_rows={ 'headers': True, 'data': 0 },
        style_table={'maxHeight': '300px','overflowX': 'scroll'},
        style_cell={
        'backgroundColor':app_colors['background'],
        'color':app_colors['text'],
        'textAlign': 'left',
        'height': 'auto',
        'whiteSpace': 'normal'}
        )]),

    html.Div(className='row', children=[
            html.Div(className='col', children = html.H2('Select one of the above row to plot the point in the map and get polarity and policy recommendations',
            style={'color':"#CECECE", "margin-left": "15px"}))
            ]),

    html.Div([
        html.Div([
        html.Div([
            html.P(id='article-div')
                ], className='col align-self-start', style={'backgroundColor':app_colors['background'],
                'color':app_colors['text'], "height": "300px", "overflow": "auto"}),
            html.Div([
                html.H2(id='predict-div')
                ], className='col align-self-center', style={'backgroundColor':app_colors['background'],
                'color':app_colors['text']}),
            html.Div([
                html.Div(id = 'rec-table-id')
                ], className = "col align-self-start")], className='row')
                ], className="container"),
    ], style={'backgroundColor': app_colors['background']})


@app.callback([Output('table', 'data'),
              Output('map_id', "figure"),
              Output('article-div', "children"),
              Output('predict-div', "children"),
              Output('rec-table-id', "children")],
              [Input('table', "selected_rows"),
              Input('year_drop_id', 'value'),
              Input('admin1_drop_id', 'value')])
def update_selected_row_indices(selected_rows, input_year, district_name):
    input_year_list = input_year
    district_name_list = district_name
    if type(input_year) != list:
        input_year_list = [input_year]
    if type(district_name) != list:
        district_name_list = [district_name]


    filtered_df = df_01[df_01['Year'].isin(input_year_list) & df_01['admin1_fipsnames'].isin(district_name_list)]
    rows = filtered_df.to_dict('records')


    if len(selected_rows) == 0:
        return rows, gen_map(filtered_df), None, None,None
    else:
        temp_df = filtered_df.iloc[selected_rows]
        article_url = temp_df['SOURCEURL'].values[0]#.loc[selected_rows[0]]  #ex_df['SOURCEURL'].loc[2]


        try:
            article_text = NewsPlease.from_url(article_url).text
            http_error = False
        except:
            http_error = True
            http_error_message = "HTTP ERROR, Article can't be loaded, check whether the article still exists"


        if http_error == True:
            return rows, gen_map(temp_df), http_error_message, None, None
        elif type(article_text) == str and http_error == False:
            #index_div_output = f"selected row is {selected_rows[0]} and its url is : \n{article_url} \nits article text is:"
            clean_article = clean_text(article_text)
            new_vect = tfidf_uni_loaded.transform([clean_article])
            predicted_class = tfidf_uni_model.predict(new_vect)[0]
            predict_div_output = f"Article is {predicted_class}"
            if predicted_class == 'positive':

                rec_df = recommend_policies(clean_article)
                #print(pol_rec_list, cos_val_list)
                return rows, gen_map(temp_df), article_text, predict_div_output, generate_table(df=rec_df)#f"{article_url}"
            elif predicted_class == 'negative':
                return rows, gen_map(temp_df), article_text, predict_div_output, None
        elif type(article_text) == type(None) and http_error == False:
            error_message = f"Article can't be loaded, Please select another row"
            return rows, gen_map(temp_df), error_message, None, None








'''@app.callback(
    Output('map_id', "figure"),
    [Input('table', "data"),
    Input('table', "selected_rows")])
def map_selection(data, selected_rows):
    aux = pd.DataFrame(data)
    temp_df = aux.iloc[selected_rows]
    if len(selected_rows) == 0:
        return gen_map(aux)
    else:
         return gen_map(temp_df)
'''
server = app.server
if __name__ == '__main__':
    app.run_server()
