from flask_restful import Resource, reqparse
from datetime import datetime
from flask import Flask, Response , json ,request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from Models.ApiException import handleException
from Models.Schema import *
from Models.Function import *
from Models.Bean import *
from Models.Constant import *
from BAL.BALExplorers import *
import time




class SaveExplorer(MethodResource,Resource):
    '''
    This API is used to save Explorer
    '''
    @handleException
    @doc(tags=['Explorers'], description=" save Explorer API.")
    @use_kwargs(SaveExplorerSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers'))
    def post(self, **kwargs):
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        if(loginAs==Constant.ADMINUSER):
            req.add_argument('id',type=int,default=None,required=False)
            req.add_argument('cryptocurrencyId',type=int,default=None,required=False,help='Please select cryptocurrency.')
            req.add_argument('name',type=str,default=None,required=False,help='Please enter name.')
            req.add_argument('link',type=str,default=None,required=True,help='Please enter Link.')
            data=req.parse_args()
            if(data['name']==None):
                data['name']="null"
            if(data['id']!=None):
                sqlQuery="update explorers set cryptocurrency_id="+str(data['cryptocurrencyId'])+", name='"+data['name']+"', link='"+data['link']+"' where id="+str(data['id'])
            else:
                sqlQuery="insert into explorers values('"+strdatetime+"',"+str(loginId)+","+str(data['cryptocurrencyId'])+",'"+str(data['name'])+"','"+str(data['link'])+"',null,null,0,null,null,1)"
            output=Database.insertData(sqlQuery)
            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured While Saving. ",201)
            return Return.returnResponse("Explorer Updated successfully. ",201) 
        else:
            return Return.returnResponse("Invalid url ",201) 




        
class GetExplorerList(MethodResource,Resource):
    '''
    This API is used to get Explorer
    '''
    @handleException
    @doc(tags=['Explorers'], description=" save Explorer API.")
    @use_kwargs(getExplorerSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers'))
    def post(self, **kwargs):
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        if(loginAs==Constant.ADMINUSER or loginAs==Constant.CUSTOMER):
            req.add_argument('id',type=int,default=None,required=False)
            req.add_argument('cryptocurrencyId',type=int,default=None,required=False)
            data=req.parse_args()
            func=BALExplorer()
            if loginAs=="adminuser":
                explorerList=func.getExplorerList(data['id'],data['cryptocurrencyId'],flag=1)
            else:
                explorerList=func.getExplorerList(data['id'],data['cryptocurrencyId'])
            return Return.returnResponse(explorerList,200)
        else:
            return Return.returnResponse("Invalid url ",201)



        
class DisableEnableExplorer(MethodResource,Resource):
    '''
    This API is used to Disable Enable Explorers
    '''
    @handleException
    @doc(tags=['Explorers'], description=" Disable/Enable Explorer API.")
    @use_kwargs(IdSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers'))
    def post(self, **kwargs):
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        methodName=Function.getEndpoint(request.base_url)

        if(methodName=="disableExplorer" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update explorers set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Explorer disable successfully.",200)
        elif(methodName=="enableExplorer" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update explorers set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Explorer enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)


        

class DeleteExplorer(MethodResource,Resource):
    '''
    This API is used to delete Explorer
    '''
    @handleException
    @doc(tags=['Explorers'], description=" Delete Explorer API.")
    @use_kwargs(IdSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers'))
    def post(self, **kwargs):
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        if(loginAs==Constant.ADMINUSER):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update explorers set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Explorer deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)



