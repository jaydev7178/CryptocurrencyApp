from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database

class BALWatchlist:
    def getWatchList(self,id=None,cryptocurrencyId=None,customerId=None,deleted=0,status=1,flag=2):
        watchList=[]
        where=""
        field="id, cryptocurrency_id, customer_id, min_threshold, max_threshold "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from watch_list "        
        if(status!=None):
            where=where+" status="+str(status)+" and "
        if(id!=None):
            where=where+" id="+str(id)+" and "
        if(customerId!=None):
            where=where+" customer_id="+str(customerId)+" and "
        if(cryptocurrencyId!=None):
            where=where+" cryptocurrency_id="+str(cryptocurrencyId)+" and "
        if(deleted!=None):
            where=where+" deleted="+str(deleted)+" and "
        if(len(where)>0):
            query=query+" where "+where.rsplit("and ",1)[0]
        cursor=Database.getCursor(query)
        if(cursor=="201"):
            return watchList
        for row in cursor:
            element=WatchListModel()
            element.id=row[0]
            element.cryptocurrencyId=row[1]
            element.customerId=row[2]
            element.minThreshold =row[3]
            element.maxThreshold =row[4]
            if flag==1:
                element.status=row[5]
            watchList.append(element.__dict__)

        return watchList
