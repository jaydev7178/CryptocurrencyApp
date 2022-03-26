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
from BAL.BALCommunity import *
import time


class SaveCommunity(MethodResource,Resource):
    '''
    This API is used to save Community
    '''
    @handleException
    @doc(tags=['Community'], description=" save Community API.")
    @use_kwargs(SaveCommunitySchema,location=('json'))
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
            if(data['id']!=None):
                sqlQuery="update community set cryptocurrency_id="+str(data['cryptocurrencyId'])+", name='"+data['name']+"', link='"+data['link']+"',image='"+str(data['image'])+"' where id="+str(data['id'])
            else:
                sqlQuery="insert into community values('"+strdatetime+"',"+str(loginId)+","+str(data['cryptocurrencyId'])+",'"+str(data['name'])+"','"+str(data['link'])+"',null,null,null,0,null,null,1)"
            output=Database.insertData(sqlQuery)
            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured While Saving. ",201)
            return Return.returnResponse("Community Updated successfully. ",201) 
        else:
            return Return.returnResponse("Invalid url ",201) 



class GetCommunityList(MethodResource,Resource):
    '''
    This API is used to get list of the Community
    '''
    @handleException
    @doc(tags=['Community'], description=" Get Community List API.")
    @use_kwargs(getCoummunitySchema,location=('json'))
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
            func=BALCommunity()
            if(loginAs==ConConstant.ADMINUSER):
                communityList=func.getCommunityList(data['id'],data['cryptocurrencyId'],flag=1)
            else:
                communityList=func.getCommunityList(data['id'],data['cryptocurrencyId'])

            return Return.returnResponse(communityList,200)
        else:
            return Return.returnResponse("Invalid url ",201)



class DisableEnableCommunity(MethodResource,Resource):
    '''
    This API is used to Disable Enable Community
    '''
    @handleException
    @doc(tags=['Community'], description=" Disable/Enable Community API.")
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
        if(methodName=="disableCommunity" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update community set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Community disable successfully.",200)
        elif(methodName=="enableCommunity" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update community set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Community enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)


class DeleteCommunity(MethodResource,Resource):
    '''
    This API is used to Delete Community
    '''
    @handleException
    @doc(tags=['Community'], description=" Get Community List API.")
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
            query="update community set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Community deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)