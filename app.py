import os
import plotly
import plotly.graph_objects as go
import pandas as pd
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import logging
import boto3
from plot import plot_popularname, popular_names, plot_sentiment, wordcloud_generator
from dotenv import load_dotenv
from dash import Dash
import plotly.express as px

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)

ACCESS_ID = "AKIA4RPDRDJ73X7BRDQW"
ACCESS_KEY ="3xAM792E8iTUx24tc6J4EBWo64IZ8Zav7uIQZssl"

s3 = boto3.client('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)
LOG.info("s3 created")
# 's3' is a key word. create connection to S3 using default config and all buckets within S3
bucket = "we-rate-dogs-data"
file = "processed-data/master.csv"
obj = s3.get_object(Bucket= bucket, Key= file) 
# get object and file (key) from bucket

twitter_archive = pd.read_csv(obj['Body'])
LOG.info(twitter_archive.head())

app = Dash(__name__)
LOG.info(app)

app.layout = html.Div([
    html.Center([
        dbc.Row([
        dbc.Col(html.H1('We Rate Dogs Dashboard')),
        dbc.Col(html.H3('Analysis'))])]),
    dcc.Tabs([
        dcc.Tab(label='Popular Graph', children=[
            dcc.Graph(
                figure=plot_popularname(twitter_archive)
            )
        ]),
        dcc.Tab(label='Sentiment Plot', children=[
            dcc.Graph(
                figure=plot_sentiment(twitter_archive)
            )
        ]),
        dcc.Tab(label='Popular Names', children=[
            dcc.Graph(
                figure=popular_names(twitter_archive)
            )
        ]),
        dcc.Tab(label='Word Clouds', children=[
            dcc.Graph(
                figure=wordcloud_generator(twitter_archive)
            )
        ])
    ])
])

LOG.info("Dashboard created")

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
    