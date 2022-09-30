from asyncio.windows_events import NULL
from http.client import HTTPResponse
from xmlrpc.client import ResponseError
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from numpy import not_equal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import csv ,operator ,json
import os
import glob

def home(request):
    return HttpResponse("Welcome to the API. Please specify appropriate routes to get values.")

@api_view(['GET'])
def top_price(request, value):

    path = os.getcwd() + '/Data/'
    location = path+'/'+"Analysis.csv"
    files = os.path.join(location)
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.drop('OPEN_INT', inplace=True, axis=1)
    df.drop('CLOSE', inplace=True, axis=1)
    df.drop('%_OI_change', inplace=True, axis=1)
    df.drop('Quantity/Trades', inplace=True, axis=1)
    df.drop('OI_Trend', inplace=True, axis=1)
    sorted_df = df. sort_values(by=["%_Price_change"], ascending=False)

    if request.method == 'GET':
        if(value == 'gainers'):
            sorted_df = sorted_df.head(5)
            jsonData = sorted_df.to_json(orient='records')
            jsonData = json.loads(jsonData)  
            return Response(jsonData)
        elif(value == 'losers'):
            sorted_df = sorted_df.tail(5)
            sorted_df = sorted_df.loc[::-1]
            jsonData = sorted_df.to_json(orient='records')
            jsonData = json.loads(jsonData)  
            return Response(jsonData)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def top_oi(request, value):

    path = os.getcwd() + '/Data/'
    location = path+'/'+"Analysis.csv"
    files = os.path.join(location)
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.drop('OPEN_INT', inplace=True, axis=1)
    df.drop('CLOSE', inplace=True, axis=1)
    df.drop('%_Price_change', inplace=True, axis=1)
    df.drop('Quantity/Trades', inplace=True, axis=1)
    df.drop('OI_Trend', inplace=True, axis=1)
    sorted_df = df. sort_values(by=["%_OI_change"], ascending=False)
    
    if request.method == 'GET':
        if(value == 'gainers'):
            sorted_df = sorted_df.head(5)
            jsonData = sorted_df.to_json(orient='records')
            jsonData = json.loads(jsonData)  
            return Response(jsonData)
        elif(value == 'losers'):
            sorted_df = sorted_df.tail(5)
            sorted_df = sorted_df.loc[::-1]
            jsonData = sorted_df.to_json(orient='records')
            jsonData = json.loads(jsonData) 
            return Response(jsonData)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def top_lb(request):

    path = os.getcwd() + '/Data/'
    location = path+'/'+"Analysis.csv"
    files = os.path.join(location)
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.drop('OPEN_INT', inplace=True, axis=1)
    df.drop('CLOSE', inplace=True, axis=1)
    df.drop('Quantity/Trades', inplace=True, axis=1)
    df.drop(df[(df['OI_Trend'] != 'Long Build Up')].index, inplace=True)
    df.drop('OI_Trend', inplace=True, axis=1)
    df["Long Buildup"] = df["%_Price_change"] * df["%_OI_change"]
    sorted_df = df. sort_values(by=["Long Buildup"], ascending=False)
    sorted_df.drop('Long Buildup', inplace=True, axis=1)

    if request.method == 'GET':
        sorted_df = sorted_df.head(5)
        jsonData = sorted_df.to_json(orient='records')
        jsonData = json.loads(jsonData) 
        return Response(jsonData)

@api_view(['GET'])
def top_lc(request):

    path = os.getcwd() + '/Data/'
    location = path+'/'+"Analysis.csv"
    files = os.path.join(location)
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.drop('OPEN_INT', inplace=True, axis=1)
    df.drop('CLOSE', inplace=True, axis=1)
    df.drop('Quantity/Trades', inplace=True, axis=1)
    df.drop(df[(df['OI_Trend'] != 'Long Cover Up')].index, inplace=True)
    df.drop('OI_Trend', inplace=True, axis=1)
    df["Long Coverup"] = df["%_Price_change"] * df["%_OI_change"]
    sorted_df = df. sort_values(by=["Long Coverup"], ascending=False)
    sorted_df.drop('Long Coverup', inplace=True, axis=1)

    if request.method == 'GET':
        sorted_df = sorted_df.head(5)
        jsonData = sorted_df.to_json(orient='records')
        jsonData = json.loads(jsonData)  
        return Response(jsonData)

@api_view(['GET'])
def top_sb(request):

    path = os.getcwd() + '/Data/'
    location = path+'/'+"Analysis.csv"
    files = os.path.join(location)
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.drop('OPEN_INT', inplace=True, axis=1)
    df.drop('CLOSE', inplace=True, axis=1)
    df.drop('Quantity/Trades', inplace=True, axis=1)
    df.drop(df[(df['OI_Trend'] != 'Short Build Up')].index, inplace=True)
    df.drop('OI_Trend', inplace=True, axis=1)
    df["Short Buildup"] = df["%_Price_change"] * df["%_OI_change"] * -1
    sorted_df = df. sort_values(by=["Short Buildup"], ascending=False)
    sorted_df.drop('Short Buildup', inplace=True, axis=1)

    if request.method == 'GET':
        sorted_df = sorted_df.head(5)
        jsonData = sorted_df.to_json(orient='records')
        jsonData = json.loads(jsonData) 
        return Response(jsonData)

@api_view(['GET'])
def top_sc(request):

    path = os.getcwd() + '/Data/'
    location = path+'/'+"Analysis.csv"
    files = os.path.join(location)
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.drop('OPEN_INT', inplace=True, axis=1)
    df.drop('CLOSE', inplace=True, axis=1)
    df.drop('Quantity/Trades', inplace=True, axis=1)
    df.drop(df[(df['OI_Trend'] != 'Short Covering')].index, inplace=True)
    df.drop('OI_Trend', inplace=True, axis=1)
    df["Short Coverup"] = df["%_Price_change"] * df["%_OI_change"] * -1
    sorted_df = df. sort_values(by=["Short Coverup"], ascending=False)
    sorted_df.drop('Short Coverup', inplace=True, axis=1)

    if request.method == 'GET':
        sorted_df = sorted_df.head(5)
        jsonData = sorted_df.to_json(orient='records')
        jsonData = json.loads(jsonData) 
        return Response(jsonData)