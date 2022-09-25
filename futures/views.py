from msvcrt import putch
from xmlrpc.client import ResponseError
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import csv ,operator ,json
import os
import glob

@api_view(['GET'])
def invalid(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def top_price(request):

    if request.GET.get("value", None) is not None :
        value = request.GET.get('value')
    else:
        value = ''
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
    sorted_df = df. sort_values(by=["Price_change"], ascending=False)
    # location = path + '/Top_Price_Gainers.csv'
    # sorted_df.to_csv(location,index=False)

    if request.method == 'GET':
        if(value == 'gainers'):
            sorted_df = sorted_df.head(5)
            location_j = path + '/Top_PriceGainers.json'
            # csv_to_json(location,location_j)
            sorted_df.to_json(path + '/Top_PriceGainers.json', orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)
            data = open(path + '/Top_PriceGainers.json').read()
            jsonData = json.loads(data)
            os.remove(path + '/Top_PriceGainers.json') 
            return Response(jsonData)
        elif(value == 'losers'):
            sorted_df = sorted_df.tail(5)
            location_j = path + '/Top_PriceGainers.json'
            # csv_to_json(location,location_j)
            sorted_df.to_json(path + '/Top_PriceGainers.json', orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)
            data = open(path + '/Top_PriceGainers.json').read()
            jsonData = json.loads(data)
            os.remove(path + '/Top_PriceGainers.json') 
            return Response(jsonData)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

def csv_to_json(csv_file_path, json_file_path):
    #create a dictionary
    data_dict = {}
 
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        for rows in csv_reader:
 
            #assuming a column named 'No'
            #to be the primary key
            key = rows['SYMBOL']
            data_dict[key] = rows
 
    #open a json file handler and use json.dumps
    #method to dump the data
    #Step 3
    with open(json_file_path, 'w', encoding = 'utf-8') as json_file_handler:
        #Step 4
        json_file_handler.write(json.dumps(data_dict, indent = 4))