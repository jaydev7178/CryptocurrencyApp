from flask_restful import Resource, reqparse
from datetime import datetime
from flask import Flask, Response , json ,request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from Models.ApiException import handleException
from Models.Schema import *
from Models.Function import *
from Models.Constant import *
from Models.Bean import *
from BAL.BALWatchlist import *
import time



class SaveWatchList(MethodResource,Resource):
    '''
    This API is used to save WatchList
    '''
    @handleException
    @doc(tags=['WatchList'], description=" save WatchList API.")
    @use_kwargs(SaveWatchListSchema,location=('json'))
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
            req.add_argument('customerId',type=int,default=None,required=False,help='Invaild customer, please try again.')
            req.add_argument('cryptocurrencyId',type=int,default=None,required=False,help='Invaild customer, please try again.')
            req.add_argument('minThreshold',type=float,default=None,required=True,help='Please select minimum threshold of cryptocurrency')
            req.add_argument('maxThreshold',type=float,default=None,required=True,help='Please select maximum threshold of cryptocurrency')
            data=req.parse_args()
            if(data['minThreshold']>data['maxThreshold']):
                return Return.returnResponse("Please check Minimum threshold is greater than Maximum threshold. ",201)
            #current DateTime
            strdatetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if(data['id']!=None):
                query="update watch_list set min_threshold="+str(data['minThreshold'])+" , max_threshold="+str(data['maxThreshold'])+" where id ="+str(data['id'])+" and deleted=0 and status=1"
            else :
                query ="insert into watch_list values('"+strdatetime+"', 8, "+str(data['cryptocurrencyId'])+", "+str(data['customerId'])+", "+str(data['minThreshold'])+", "+str(data['maxThreshold'])+", null, null, 0,null,null,1)"
            output=Database.insertData(query)

            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured while saving data ",201)

            return Return.returnResponse("Watch list Added Successfully",200)
        else:
            return Return.returnResponse("Invalid URL ",201)



        
class GetWatchList(MethodResource,Resource):
    '''
    This API is used to get WatchList
    '''
    @handleException
    @doc(tags=['WatchList'], description=" get WatchList API.")
    @use_kwargs(getWatchListSchema,location=('json'))
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
            req.add_argument('customerId',type=int,default=None,required=False)
            data=req.parse_args()
            func=BALWatchlist()
            if(loginAs==Constant.ADMINUSER ):
                watchList=func.getWatchList(data['id'],data['cryptocurrencyId'],data['customerId'],flag=1)
            else:
                watchList=func.getWatchList(data['id'],data['cryptocurrencyId'],loginId)
            return Return.returnResponse(watchList,200)
        else:
            return Return.returnResponse("Invalid URL ",201)


        
class DisableEnableWatchList(MethodResource,Resource):
    '''
    This API is used to Disable Enable Explorers
    '''
    @handleException
    @doc(tags=['WatchList'], description=" Disable/Enable WatchList API.")
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

        if(methodName=="disableWatchList" and loginAs==Constant.ADMINUSER or loginAs==Constant.CUSTOMER):
            req.add_argument('id',type=int,default=None,required=True,help='Please select Watch List.')
            data=req.parse_args()
            query="update watch_list set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Watch List disable successfully.",200)

        elif(methodName=="enableWatchList" and loginAs==Constant.ADMINUSER or loginAs==Constant.CUSTOMER):
            req.add_argument('id',type=int,default=None,required=True,help='Please select customer.')
            data=req.parse_args()
            query="update watch_list set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Watch List enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)


        
class DeleteWatchList(MethodResource,Resource):
    '''
    This API is used to save WatchList
    '''
    @handleException
    @doc(tags=['WatchList'], description=" Delete WatchList API.")
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
            req.add_argument('id',type=float,default=None,required=True,help='Please select watch List.')
            data=req.parse_args()
            sqlQuery="update watch_list set deleted=1, deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])
            output=Database.insertData(sqlQuery)
            if(sqlQuery=="201"):
                return Return.returnResponse("Some Internal Issue Occured while deleting data ",201)
            return Return.returnResponse("Watch List deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)