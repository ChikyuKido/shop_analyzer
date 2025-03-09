import re

from db import ShopEntryTypes
import plotly.express as px
import pandas as pd

def show_graph(price_history,type):
    if type == str(ShopEntryTypes.GRAMM):
        show_graph_for_gram(price_history)
    elif type == str(ShopEntryTypes.LITER):
        show_graph_for_liter(price_history)
    elif type == str(ShopEntryTypes.STUECK):
        show_graph_for_piece(price_history)
    elif type == str(ShopEntryTypes.METER):
        show_graph_for_meter(price_history)
    elif type == str(ShopEntryTypes.KISTE):
        show_graph_for_kiste(price_history)

def show_graph_for_gram(price_history):
    df = pd.DataFrame(price_history)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['kg'] = df['additional_info'].astype(float).div(1000)
    df['price_per_kg'] = df['price'] / df['kg']
    fig = px.line(df, x='date', y=['price', 'kg', 'price_per_kg'],
              labels={'value': 'Value', 'date': 'Date'},
              title='Price, Grams, and Price per kg Over Time')
    fig.show()
def show_graph_for_liter(price_history):
    df = pd.DataFrame(price_history)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['liter'] = df['additional_info'].astype(float)
    df['price_per_liter'] = df['price'] / df['liter']
    fig = px.line(df, x='date', y=['price', 'liter', 'price_per_liter'],
                  labels={'value': 'Value', 'date': 'Date'},
                  title='Price, Liter, and Liter per kg Over Time')
    fig.show()
def show_graph_for_piece(price_history):
    df = pd.DataFrame(price_history)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['pieces'] = df['additional_info'].astype(int)
    df['price_per_piece'] = df['price'] / df['pieces']
    fig = px.line(df, x='date', y=['price', 'pieces', 'price_per_piece'],
                  labels={'value': 'Value', 'date': 'Date'},
                  title='Price, Pieces, and Price per pieces Over Time')
    fig.show()
def show_graph_for_meter(price_history):
    df = pd.DataFrame(price_history)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['meters'] = df['additional_info'].astype(float)
    df['price_per_meter'] = df['price'] / df['meters']
    fig = px.line(df, x='date', y=['price', 'meters', 'price_per_meter'],
                  labels={'value': 'Value', 'date': 'Date'},
                  title='Price, Meters, and Price per meters Over Time')
    fig.show()

def show_graph_for_kiste(price_history):
    df = pd.DataFrame(price_history)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['kisten'] = df['additional_info'].astype(int)
    df['price_per_kiste'] = df['price'] / df['kisten']
    fig = px.line(df, x='date', y=['price', 'kisten', 'price_per_kiste'],
                  labels={'value': 'Value', 'date': 'Date'},
                  title='Price, Kisten, and Price per kiste Over Time')
    fig.show()