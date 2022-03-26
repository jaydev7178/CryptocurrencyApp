from flask import Flask, jsonify, request, make_response,jsonify,json
from flask_restful import Resource, Api, marshal_with, fields,reqparse
from Models.Bean import *
from Models.Return import Return
from Models.Database import Database

class BALCustomers:
    def getCustomersList(self,id=None,deleted=0,status=1,flag=2):
        customersList=[]
        where=""
        field=" id, name, mobile, email "
        if(flag==1):
            field=field+",status "
        query="select "+field+" from customers "      
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
                return customersList         
        for row in cursor:
            element=CustomerModel()
            element.id=row[0]
            element.name=row[1]
            element.mobile=row[2]
            element.email=row[3] 
            if(flag==1):
                element.status=row[4]
            customersList.append(element.__dict__)
        return customersList
            
    def getCustomerEmailList(self):
        customerEmails=[]
        func=BALCustomers()
        customerList=func.getCustomersList(None)
        for customerObj in customerList:
            customerEmails.append(customerObj['email'])
        return customerEmails