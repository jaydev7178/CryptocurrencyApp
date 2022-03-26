from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database

class BALCryptocurrencies:
    def getCryptocurrenciesList(self,id=None,deleted=0,status=1,flag=2):
        cryptocurrenciesList=[]
        where=""
        field=" id, coingecko_crypto_id, name, symbol, image, website, source_code, market_cap, market_cap_rank, fully_diluted_valuation, total_volume, circulating_supply, total_supply, max_supply, ath, ath_change_percentage, ath_date, atl, atl_change_percentage, atl_date, roi,last_updated "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from cryptocurrencies "      
        if(status!=None):
            where=where+" status="+str(status)+" and "
        if(id!=None):
            where=where+" id="+str(id)+" and "
        if(deleted!=None):
            where=where+" deleted="+str(deleted)+" and "
        if(len(where)>0):
            query=query+" where "+where.rsplit("and ",1)[0]
        cursor=Database.getCursor(query)
        if(cursor=="201"):
                return cryptocurrenciesList         
        for row in cursor:
            element=CryptoCurrencyModel()
            element.id=row[0]
            element.coingcoingeckoCryptoId=row[1]
            element.name=row[2]
            element.symbol=row[3]
            element.image=row[4]
            element.website=row[5]
            element.sourceCode=row[6]
            element.marketCap=row[7]
            element.marketCapRank=row[8]
            element.fullyDiluatedValuation=row[9]
            element.totalVolume=row[10]
            element.circulatingSupply=row[11]
            element.totalSupply=row[12]
            element.maxSupply=row[13]
            element.ath=row[14]
            element.athChangePercentage=row[15]
            element.athDate=row[16]
            element.atl=row[17]
            element.atlChangePercentage=row[18]
            element.atlDate=row[19]
            element.roi=row[20]
            element.lastUpdated=row[21]
            if(flag==1):
                element.status=row[22]
            cryptocurrenciesList.append(element.__dict__)
        
        return cryptocurrenciesList


