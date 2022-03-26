from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database

class BALExplorer:

    def getExplorerList(self,id=None, cryptocurrencyId=None,deleted=0,status=1,flag=2):
        explorerList=[]
        where=""
        field="id, cryptocurrency_id, name, link "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from explorers "        
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
            return explorerList
        for row in cursor:
            element=ExplorerModel()
            element.id=row[0]
            element.cryptocurrencyId=row[1]
            element.name=row[2]
            element.link =row[3]
            if(flag==1):
                element.status=row[4]
            explorerList.append(element.__dict__)

        return explorerList
