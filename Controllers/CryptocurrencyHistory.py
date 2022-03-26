from flask_restful import Resource, reqparse
from datetime import datetime
from flask import Flask, Response , json ,request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from Models.ApiException import handleException
from Models.Schema import *
from Models.Function import *
from Models.Bean import *
from BAL.BALCryptocurrencyhistory import *
import time



class SaveCryptocurrencyHistory(MethodResource,Resource):
    '''
    This API is used to save CryptocurrencyHistory
    '''
    @handleException
    @doc(tags=['CryptocurrencyHistory'], description=" save CryptocurrencyHistory API.")
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
            req.add_argument('cryptocurrencyId',type=int,default=None,required=True,help='Please select cryptocurrency.')
            req.add_argument('currentPrice',type=float,default=None,required=False)
            req.add_argument('high24h',type=float,default=None,required=False)
            req.add_argument('low24h',type=float,default=None,required=False)
            req.add_argument('priceChange24h',type=float,default=None,required=False)
            req.add_argument('marketCapChange24h',type=float,default=None,required=False)
            req.add_argument('marketCapChangePercentage24h',type=float,default=None,required=False)
            req.add_argument('priceChangePercentage1hInCurrency',type=float,default=None,required=False)
            req.add_argument('priceChangePercentage24hInCurrency',type=float,default=None,required=False)
            req.add_argument('priceChangePercentage7dInCurrency',type=float,default=None,required=False)
            req.add_argument('priceChangePercentage14dInCurrency',type=float,default=None,required=False)
            req.add_argument('priceChangePercentage30dInCurrency',type=float,default=None,required=False)
            req.add_argument('priceChangePercentage200dInCurrency',type=float,default=None,required=False)
            req.add_argument('priceChangePercentage1yInCurrency',type=float,default=None,required=False)
            data=req.parse_args()
            if(data['id']!=None):
                sqlQuery="update cryptocurrency_history set cryptocurrency_id="+str(data['cryptocurrencyId'])+", current_price="+str(data['currentPrice'])+", high_24h="+str(data['high24h'])+", low_24h="+str(data['low24h'])+", price_change_24h="+str(data['priceChange24h'])+", market_cap_change_24h="+str(data['marketCapChange24h'])+", market_cap_change_percentage_24h="+str(data['marketCapChangePercentage24h'])+", price_change_percentage_1h_in_currency="+str(data['priceChangePercentage1hInCurrency'])+", price_change_percentage_24h_in_currency="+str(data['priceChangePercentage24hInCurrency'])+", price_change_percentage_7d_in_currency="+str(data['priceChangePercentage7dInCurrency'])+", price_change_percentage_14d_in_currency="+str(data['priceChangePercentage14dInCurrency'])+", price_change_percentage_30d_in_currency="+str(data['priceChangePercentage30dInCurrency'])+", price_change_percentage_200d_in_currency="+str(data['priceChangePercentage300dInCurrency'])+", price_change_percentage_1y_in_currency="+str(data['priceChangePercentage1yInCurrency'])+" where id="+str(data['id'])
            else:
                sqlQuery="insert into cryptocurrency_history values('"+strdatetime+"',"+str(loginId)+","+str(data['cryptocurrencyId'])+","+str(data['currentPrice'])+","+str(data['high24h'])+","+str(data['low24h'])+","+str(data['priceChange24h'])+","+str(data['marketCapChange24h'])+","+str(data['marketCapChangePercentage24h'])+","+str(data['priceChangePercentage1hInCurrency'])+","+str(data['priceChangePercentage7dInCurrency'])+","+str(data['priceChangePercentage14dInCurrency'])+","+str(data['priceChangePercentage30dInCurrency'])+","+str(data['priceChangePercentage200dInCurrency'])+","+str(data[''])+","+str(data['priceChangePercentage1yInCurrency'])+",null,null,null,0,null,null,1)"
            output=Database.insertData(sqlQuery)
            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured While Saving. ",201)
            return Return.returnResponse("Community Updated successfully. ",201) 
        else:
            return Return.returnResponse("Invalid url ",201) 


                
class GetCryptocurrencyHistoryList(MethodResource,Resource):
    '''
    This API is used to get CryptocurrencyHistory List
    '''
    @handleException
    @doc(tags=['CryptocurrencyHistory'], description=" get CryptocurrencyHistory List API.")
    @use_kwargs(getCryptocurrencyHistorySchema,location=('json'))
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
            func=BALCryptocurrencyhistory()
            if(loginAs=="adminuser"):
                cryptocurrencyHistoryList=func.getCryptocurrencyHistoryList(data['id'],data['cryptocurrencyId'],flag=1)
            else:
                cryptocurrencyHistoryList=func.getCryptocurrencyHistoryList(data['id'],data['cryptocurrencyId'])
            return Return.returnResponse(cryptocurrencyHistoryList,200)
        else:
            return Return.returnResponse("Invalid url ",201)



        
class DisableEnableCryptocurrencyHistory(MethodResource,Resource):
    '''
    This API is used to Disable/Enable CryptocurrencyHistory
    '''
    @handleException
    @doc(tags=['Category'], description=" disableCategory/enableCategory CryptocurrencyHistory API.")
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

        if(methodName=="disableCryptocurrencyHistory" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurrency_history set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("CryptocurrencyHistory disable successfully.",200)
        elif(methodName=="enableCryptocurrencyHistory" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurrency_history set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("CryptocurrencyHistory enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)



        
class DeleteCryptocurrencyHistory(MethodResource,Resource):
    '''
    This API is used to save CryptocurrencyHistory
    '''
    @handleException
    @doc(tags=['CryptocurrencyHistory'], description=" Delete CryptocurrencyHistory API.")
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
            query="update cryptocurrency_history set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Cryptocurrency history deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)


