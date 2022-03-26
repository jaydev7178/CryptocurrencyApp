from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database


class BALPlatforms:

    def getPlatformsList(self, id=None, deleted=0,status=1,flag=2):
        platformList=[]
        where=""
        field="id,coingecko_platform_id,name,shortname, chain_identifier "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from platforms "        
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
                return platformList         
        for row in cursor:
            element=PlatformsModel()
            element.id =row[0]
            element.coingeckoPlatformId =row[1]
            element.name =row[2]
            element.shortname =row[3]
            element.chainIdentifier =row[4]
            if(flag==1):
                element.status =row[5]

            platformList.append(element.__dict__)
        return platformList