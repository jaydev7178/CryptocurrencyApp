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
from BAL.BALCryptocurrencyCategoryMapping import *
import time


class SaveCryptocurrencyCategoryMapping(MethodResource,Resource):
    '''
    This API is used to save SaveCryptocurrencyCategoryMapping
    '''
    @handleException
    @doc(tags=['CryptocurrencyCategoryMapping'], description=" save CryptocurrencyCategoryMapping API.")
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
            req.add_argument('categoryId',type=int,default=None,required=True,help='Please select category.')
            req.add_argument('cryptocurrencyId',type=int,default=None,required=True,help='Please select cryptocurrency.')
            data=req.parse_args()
            if(data['id']!=None):
                query="update cryptocurrency_category_mapping set crytocurrency_id="+str(data['cryptocurrencyId'])+" , category_id="+str(data['categoryId'])+" where id ="+str(data['id'])+" "
            else :
                query ="insert into cryptocurrency_category_mapping values('"+strdatetime+"', "+str(loginId)+", "+str(data['cryptocurrencyId'])+", "+str(data['categoryId'])+", null, 0,null,null,1)"
            output=Database.insertData(query)

            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured while saving data ",201)

            return Return.returnResponse("CryptocurrencyCategoryMapping Added Successfully",200)
        else:
            return Return.returnResponse("Invalid URL ",201)


        
class GetCryptocurrencyCategoryMappingList(MethodResource,Resource):
    '''
    This API is used to get CryptocurrencyCategoryMapping List
    '''
    @handleException
    @doc(tags=['CryptocurrencyCategoryMapping'], description=" get CryptocurrencyCategoryMapping List API.")
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

        if(loginAs==Constant.ADMINUSER or loginAs==Constant.CUSTOMER):
            req.add_argument('id',type=int,default=None,required=False)
            req.add_argument('cryptocurrencyId',type=int,default=None,required=False)
            req.add_argument('categoryId',type=int,default=None,required=False)
            data=req.parse_args()
            func=BALCryptocurrencyCategoryMapping()
            if(loginAs=="adminuser"):
                cryptocurrencyCategoryMappingList=func.getCryptocurrencyCategoryMappingList(data['id'],data['cryptocurrencyId'],data['categoryId'],flag=1)
            else:
                cryptocurrencyCategoryMappingList=func.getCryptocurrencyCategoryMappingList(data['id'],data['cryptocurrencyId'],data['categoryId'])
            return Return.returnResponse(cryptocurrencyCategoryMappingList,200)
        else:
            return Return.returnResponse("Invalid URL ",201)




class DisableEnableCryptocurrencyCategoryMapping(MethodResource,Resource):
    '''
    This API is used to DisableEnable CryptocurrencyCategoryMapping
    '''
    @handleException
    @doc(tags=['CryptocurrencyCategoryMapping'], description=" Disable/Enable CryptocurrencyCategoryMapping API.")
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
        if(methodName=="disableCryptocurrencyCategory" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurrency_category_mapping set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("CryptocurrencyCategory disable successfully.",200)
        elif(methodName=="enableCryptocurrencyCategory" and loginAs==Constant.ADMINUSER):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurrency_category_mapping set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("CryptocurrencyCategory enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)


        
class DeleteCryptocurrencyCategoryMapping(MethodResource,Resource):
    '''
    This API is used to delete SaveCryptocurrencyCategoryMapping
    '''
    @handleException
    @doc(tags=['CryptocurrencyCategoryMapping'], description=" delete CryptocurrencyCategoryMapping API.")
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
            query="update cryptocurrency_category_mapping set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Cryptocurrency category deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)





