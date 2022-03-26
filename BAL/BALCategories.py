from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database

class BALCategories:
    def getCategoriesList(self, id=None, deleted=0,status=1,flag=2):
        categoryList=[]
        where=""
        field="id,coingecko_category_id,name,link "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from categories "        
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
                return categoryList         
        for row in cursor:
            element=CategoriesModel()
            element.id=row[0]
            element.coingeckoCategoryId=row[1]
            element.name=row[2]
            element.link=row[3]
            if(flag==1):
                element.status=row[4]
            categoryList.append(element.__dict__)
        
        return categoryList
