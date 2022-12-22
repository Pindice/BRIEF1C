from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
import csv
import html
from sqlalchemy import create_engine
from django.db import connections
from .forms import UploadFileForm
from io import TextIOWrapper
from django.shortcuts import redirect


# Create your views here.

#CREATION DATAFRAME INITIAL A PARTIR D'UN CSV
#df=pd.read_csv('database1C/data2010_2011s1.csv',encoding='ISO-8859-1')

#NETTOYAGE DE DONNEES

#IMPORT TABLE STOCK
def produits(dataframe):
#LECTURE FICHIER CSV & NETTOYAGE DES DONNEES
    stock = dataframe
    stock=stock.drop(stock[stock.Quantity < 0].index)
    stock=stock.drop(stock[(stock.UnitPrice==0) & (stock.UnitPrice==0.001)].index)
    stock=stock.drop(stock[stock.Country=='Unspecified'].index)
    stock=stock.apply(lambda x: x.astype(str).str.upper())
    stock=stock.drop_duplicates(subset=['InvoiceNo','StockCode'],keep='first')
    stock.columns = stock.columns.str.lower()
#CREER CONNEXION AVEC BDD
    engine = create_engine('postgresql://postgres:123@localhost:5432/db1C')
#NETTOYAGE DONNNEES
    stock.drop_duplicates(subset=['stockcode'], inplace=True, keep='first')
#TO_SQL : ECRIT EN SQL ET RENVOIE DANS LA BDD
    stock[['stockcode','description','unitprice']].to_sql("stock", con=engine, if_exists='append', index=False)
    print(stock)
   
#IMPORT TABLE INVOICE
def facture(dataframe):
#LECTURE FICHIER CSV & NETTOYAGE DES DONNEES
    facture = dataframe
    facture=facture.drop(facture[facture.Quantity < 0].index)
    facture=facture.drop(facture[(facture.UnitPrice==0) & (facture.UnitPrice==0.001)].index)
    facture=facture.drop(facture[facture.Country=='Unspecified'].index)
    facture=facture.apply(lambda x: x.astype(str).str.upper())
    facture=facture.drop_duplicates(subset=['InvoiceNo','StockCode'],keep='first')
    facture.columns = facture.columns.str.lower()
#CREER CONNEXION AVEC BDD
    engine = create_engine('postgresql://postgres:123@localhost:5432/db1C')
#NETTOYAGE DONNNEES
    facture.drop_duplicates(subset=['invoiceno'], inplace=True, keep='first')
#TO_SQL : ECRIT EN SQL ET RENVOIE DANS LA BDD
    facture[['invoiceno','invoicedate','customerid','country']].to_sql("invoice", con=engine, if_exists='append', index=False)
    print(facture)

#IMPORT TABLE COMPOSE
def compose(dataframe):
#LECTURE FICHIER CSV & NETTOYAGE DES DONNEES
    compose = dataframe
    compose=compose.drop(compose[compose.Quantity < 0].index)
    compose=compose.drop(compose[(compose.UnitPrice==0) & (compose.UnitPrice==0.001)].index)
    compose=compose.drop(compose[compose.Country=='Unspecified'].index)
    compose=compose.apply(lambda x: x.astype(str).str.upper())
    compose=compose.drop_duplicates(subset=['InvoiceNo','StockCode'],keep='first')
    compose.columns = compose.columns.str.lower()
#CREER CONNEXION AVEC BDD
    engine = create_engine('postgresql://postgres:123@localhost:5432/db1C')
#NETTOYAGE DONNNEES
    compose.drop_duplicates(subset=['invoiceno','stockcode'], inplace=True, keep='first')
#TO_SQL : ECRIT EN SQL ET RENVOIE DANS LA BDD
    compose[['invoiceno','stockcode','quantity']].to_sql("compose", con=engine, if_exists='append', index=False)
    print(compose)



#REQUETE SQL POUR GRAPH VENTES / PRODUITS
def VentesProduits(request):
    sql = '''SELECT stock.stockcode, COUNT(*) 
                FROM stock
                INNER JOIN compose ON stock.stockcode = compose.stockcode
                GROUP BY stock.stockcode
                ORDER BY COUNT DESC
                LIMIT 10;'''
    
    cursor = connections['default'].cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    
    liste_datas_produits=[]
    liste_labels_produits=[]
    for elt in rows:
        for elt2 in elt:
            if isinstance(elt2, str):
                liste_labels_produits.append(elt2)
            else:
                liste_datas_produits.append(elt2)
    print("liste_datas_produits",liste_datas_produits)
    print("liste_labels_produits",liste_labels_produits)
    context = {
        'liste_datas_produits':liste_datas_produits,
        'liste_labels_produits':liste_labels_produits
    }
    return render(request,'ventesproduits.html',context)

#REQUETE SQL POUR GRAPH VENTES / PAYS
def VentesPays(request):
    sql = '''SELECT country, COUNT(*)
                FROM invoice
				GROUP BY country
                ORDER BY COUNT DESC
                LIMIT 10;'''

    cursor = connections['default'].cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)

    liste_datas_pays=[]
    liste_labels_pays=[]
    for elt in rows:
        for elt2 in elt:
            if isinstance(elt2, str):
                liste_labels_pays.append(elt2)
            else:
                liste_datas_pays.append(elt2)
        print("liste_datas_pays",liste_datas_pays)
        print("liste_labels_pays",liste_labels_pays)
    context = {
            'liste_datas_pays':liste_datas_pays,
            'liste_labels_pays':liste_labels_pays
            }
    return render(request,'ventespays.html',context)



#IMPORTATION DES DONNEES DANS LA BDD VIA TELECHARGEMENT D'UN FICHIER
def Importation(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file=request.FILES['file']
        fileUn=TextIOWrapper(file,encoding='unicode_escape',newline='') #ATTENTION FILE A UTILISER UNE SEULE FOIS (POUR DATAFRAME)
        df = pd.read_csv(fileUn, encoding='unicode_escape')
        df1 = df.copy()
        df2 = df.copy()
        df3 = df.copy()
        produits(df1)
        facture(df2)
        compose(df3)
        return HttpResponse("Import réussi, veuillez retournez à l'accueil")
    else:
        form = UploadFileForm()
    return render(request,"import.html",{'form':form})