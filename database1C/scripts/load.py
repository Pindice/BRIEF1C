import csv
import os
import pandas as pd
from models import Invoice, Stock, Compose

df=pd.read_csv('data2010_2011s1.csv',encoding='unicode_escape',sep=',')

#NETTOYAGE DONNEES
df=df.drop_duplicates()


#print(df.head())




#Add rows in DB with pandas.df.itterows
row_iter = df.iterrows()

obj1 = [
    Invoice(
        InvoiceNo = row['InvoiceNo'],
        InvoiceDate = row['InvoiceDate'],
        CustomerID = row['CustomerID'],
        Country = row['Country'],
    )
    for index, row in row_iter]

obj2 = [
    Stock(
        StockCode = row['StockCode'],
        Description = row['Description'],
        UnitPrice = row['UnitPrice']
    )
    for index, row in row_iter]

obj3 = [
    Compose(
        Quantity = row['Quantity'],
        InvoiceNo = row['InvoiceNo'],
        StockCode = row['StockCode']
    )
    for index, row in row_iter]

Invoice.objects.bulk_create(obj1)
Stock.objects.bulk_create(obj2)
Compose.objects.bulk_create(obj3)