from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database

class  BALAdminusers:
    def getAdminUsersList(self,id=None, deleted=0,status=1,flag=1):
        adminUsersList=[]
        where=""
        field="id,name,mobile,email "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from admin_users "        
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
                return adminusersList
        for row in cursor:
            element=AdminModel()
            element.id=row[0]
            element.name=row[1]
            element.mobile=row[2]
            element.email=row[3]
            if(flag==1):
                element.status=row[4]
            adminUsersList.append(element.__dict__)

        return adminUsersList

        
