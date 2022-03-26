from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database
from BAL.BALPlatforms import BALPlatforms
from BAL.BALCryptocurrencies import BALCryptocurrencies

class BALCryptocurrencyPlatformMapping:

    def getCryptocurrencyPlatformMappingList(self,id=None, cryptocurrencyId=None, platformId=None,deleted=0,status=1,flag=2):
        cryptocurrencyPlatformMappingList=[]
        where=""
        field="id, cryptocurrency_id, platform_id, contract_address "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from cryptocurrency_platform_mapping "        
        if(status!=None):
            where=where+" status="+str(status)+" and "
        if(id!=None):
            where=where+" id="+str(id)+" and "
        if(cryptocurrencyId!=None):
            where=where+" cryptocurrency_id="+str(cryptocurrencyId)+" and "
        if(platformId!=None):
            where=where+" platform_id="+str(platformId)+" and "
        if(deleted!=None):
            where=where+" deleted="+str(deleted)+" and "
        if(len(where)>0):
            query=query+" where "+where.rsplit("and ",1)[0]

        cursor=Database.getCursor(query)
        if(cursor=="201"):
            return cryptocurrencyPlatformMappingList
        for row in cursor:
            element=CryptocurrencyPlatformMappingModel()
            element.id=row[0]
            element.cryptocurrencyId=row[1]
            if(element.cryptocurrencyId!=None):
                funcCryptocurrency=BALCryptocurrencies()
                element.cryptocurrencyObj=funcCryptocurrency.getCryptocurrenciesList(id=element.cryptocurrencyId,flag=1)
            element.platformId=row[2]
            if(element.platformId!=None):
                funcPlatform=BALPlatforms()
                element.platformObj=funcPlatform.getPlatformsList(id=element.platformId,flag=1)            
            element.contractAddress=row[3]
            if(flag==1):
                element.status=row[4]

            cryptocurrencyPlatformMappingList.append(element.__dict__)

        return cryptocurrencyPlatformMappingList
