from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database
from BAL.BALCryptocurrencies import BALCryptocurrencies
from BAL.BALCategories import BALCategories

class BALCryptocurrencyCategoryMapping:

    def getCryptocurrencyCategoryMappingList(self,id=None, cryptocurrencyId=None,categoryId=None,deleted=0,status=1,flag=2):
        cryptocurrencyCategoryMappingList=[]
        where=""
        field="id, cryptocurrency_id, category_id "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from cryptocurrency_category_mapping "        
        if(status!=None):
            where=where+" status="+str(status)+" and "
        if(id!=None):
            where=where+" id="+str(id)+" and "
        if(cryptocurrencyId!=None):
            where=where+" cryptocurrency_id="+str(cryptocurrencyId)+" and "
        if(categoryId!=None):
            where=where+" category_id="+str(categoryId)+" and "
        if(deleted!=None):
            where=where+" deleted="+str(deleted)+" and "
        if(len(where)>0):
            query=query+" where "+where.rsplit("and ",1)[0]

        cursor=Database.getCursor(query)
        if(cursor=="201"):
            return cryptocurrencyCategoryMappingList
        for row in cursor:
            element=CryptocurrencyCategoryMappingModel()
            element.id=row[0]
            element.cryptocurrencyId=row[1]
            if(element.cryptocurrencyId!=None):
                funcCryptocurrency=BALCryptocurrencies()
                element.cryptocurrencyObj=funcCryptocurrency.getCryptocurrenciesList(id=element.cryptocurrencyId,flag=1)
            element.categoryId=row[2]
            if(element.categoryId!=None):
                funcCategory=BALCategories()
                element.categoryObj =funcCategory.getCategoriesList(id=element.categoryId,flag=1)
            if(flag==1):
                element.status=row[3]

            cryptocurrencyCategoryMappingList.append(element.__dict__)

        return cryptocurrencyCategoryMappingList