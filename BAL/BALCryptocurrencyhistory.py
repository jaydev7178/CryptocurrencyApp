from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database

class BALCryptocurrencyhistory:

    def getCryptocurrencyHistoryList(self, id=None, cryptocurrencyId=None,deleted=0,status=1,flag=2):
        cryptocurrencyHistoryList=[]
        where=""
        field="id, cryptocurrency_id,current_price, high_24h, low_24h, price_change_24h, market_cap_change_24h, market_cap_change_percentage_24h, price_change_percentage_1h_in_currency, price_change_percentage_24h_in_currency, price_change_percentage_7d_in_currency, price_change_percentage_14d_in_currency, price_change_percentage_30d_in_currency, price_change_percentage_200d_in_currency, price_change_percentage_1y_in_currency "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from cryptocurrency_history "        
        if(status!=None):
            where=where+" status="+str(status)+" and "
        if(id!=None):
            where=where+" id="+str(id)+" and "
        if(cryptocurrencyId!=None):
            where=where+" cryptocurrency_id="+str(cryptocurrencyId)+" and "
        if(deleted!=None):
            where=where+" deleted="+str(deleted)+" and "
        if(len(where)>0):
            query=query+" where "+where.rsplit("and ",1)[0]
        cursor=Database.getCursor(query)
        if(cursor=="201"):
            return cryptocurrencyHistoryList
        for row in cursor:
            element=CryptocurrencyHistoryModel()
            element.id=row[0]
            element.cryptocurrencyId=row[1]
            element.current_price=row[2]
            element.high_24h =row[3]
            element.low_24h =row[4]
            element.price_change_24h =row[5]
            element.market_cap_change_24h =row[6]
            element.market_cap_change_percentage_24h =row[7]
            element.price_change_percentage_1h_in_currency =row[8]
            element.price_change_percentage_24h_in_currency =row[9]
            element.price_change_percentage_7d_in_currency =row[10]
            element.price_change_percentage_14d_in_currency =row[11]
            element.price_change_percentage_30d_in_currency =row[12]
            element.price_change_percentage_200d_in_currency =row[13]
            element.price_change_percentage_1y_in_currency =row[14]           
            if(flag==1):
                element.status=row[15]
            cryptocurrencyHistoryList.append(element.__dict__)

        return cryptocurrencyHistoryList

