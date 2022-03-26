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
from BAL.BALCryptocurrencyPlatformMapping import *
import time


class SaveCryptocurrencyPlatformMapping(MethodResource,Resource):
    '''
    This API is used to save CryptocurrencyPlatformMapping
    '''
    @handleException
    @doc(tags=['CryptocurrencyPlatformMapping'], description=" save CryptocurrencyPlatformMapping API.")
    @use_kwargs(SaveCryptocurrencyCategoryMappingSchema,location=('json'))
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
            req.add_argument('platformId',type=int,default=None,required=True,help='Please select platform.')
            req.add_argument('cryptocurrencyId',type=int,default=None,required=True,help='Please select cryptocurrency.')
            data=req.parse_args()
            if(data['id']!=None):
                query="update cryptocurrency_platform_mapping set crytocurrency_id="+str(data['cryptocurrencyId'])+" , platform_id="+str(data['platformId'])+" where id ="+str(data['id'])+" "
            else :
                query ="insert into cryptocurrency_platform_mapping values('"+strdatetime+"', "+str(loginId)+", "+str(data['cryptocurrencyId'])+", "+str(data['platformId'])+", null, 0,null,null,1)"
            output=Database.insertData(query)

            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured while saving data ",201)

            return Return.returnResponse("CryptocurrencyPlaformMapping Added Successfully",200)
        else:
            return Return.returnResponse("Invalid URL ",201)



        
class GetCryptocurrencyPlatformMappingList(MethodResource,Resource):
    '''
    This API is used to get CryptocurrencyPlatformMapping
    '''
    @handleException
    @doc(tags=['CryptocurrencyPlatformMapping'], description=" get CryptocurrencyPlatformMapping API.")
    @use_kwargs(getCryptocurrencyPlatformMappingSchema,location=('json'))
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
            req.add_argument('platformId',type=int,default=None,required=False)
            data=req.parse_args()
            func=BALCryptocurrencyPlatformMapping()
            if(loginAs=="adminuser"):
                cryptocurrencyPlatformMappingList=func.getCryptocurrencyPlatformMappingList(data['id'],data['cryptocurrencyId'],data['platformId'],flag=1)
            else:
                cryptocurrencyPlatformMappingList=func.getCryptocurrencyPlatformMappingList(data['id'],data['cryptocurrencyId'],data['platformId'])
            return Return.returnResponse(cryptocurrencyPlatformMappingList,200)
        else:
            return Return.returnResponse("Invalid URL ",201)



                
class DisableEnableCryptocurrencyPlatformMapping(MethodResource,Resource):
    '''
    This API is used to Disable/Enable CryptocurrencyPlatformMapping
    '''
    @handleException
    @doc(tags=['Category'], description=" disableCategory/enableCategory CryptocurrencyPlatformMapping API.")
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

        if(methodName=="disableCryptocurrencyPlatform" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurrency_platform_mapping set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("CryptocurrencyPlatform disable successfully.",200)
        elif(methodName=="enableCryptocurrencyPlatform" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurrency_platform_mapping set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("CryptocurrencyPlatform enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)



        
class DeleteCryptocurrencyPlatformMapping(MethodResource,Resource):
    '''
    This API is used to delete CryptocurrencyPlatformMapping
    '''
    @handleException
    @doc(tags=['CryptocurrencyPlatformMapping'], description=" Delete CryptocurrencyPlatformMapping API.")
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
            query="update cryptocurrency_platform_mapping set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Cryptocurrency platform deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)
