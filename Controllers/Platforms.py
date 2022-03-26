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
from BAL.BALPlatforms import *
import time




class SavePlatform(MethodResource,Resource):
    '''
    This API is used to save Platform
    '''
    @handleException
    @doc(tags=['Platforms'], description=" save Platform API.")
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
            req.add_argument('coingeckoPlatformId',type=str,default=None,required=True,help='Please enter coingecko platform id.')
            req.add_argument('name',type=str,default=None,required=True,help='Please enter name.')
            req.add_argument('shortname',type=str,default=None,required=True,help='Please enter shortname.')
            req.add_argument('chainIdentifier',type=int,default=None,required=True,help='Please enter chain indentifier.')
            data=req.parse_args()
            if(data['chainIdentifier']==None):
                data['chainIdentifier']='null'
            if(data['shortname']==None or data['shortname']==""):
                data['shortname']='null';
            else :
                data['shortname']="'"+data['shortname']+"'"
            if(data['id']!=None):
                sqlQuery="update platforms set coingecko_platform_id='"+str(data['coingeckoPlatformId'])+"', name='"+str(data['name'])+"', shortname="+str(data['shortname'])+", chain_identifier="+str(data['chainIdentifier'])+" where id="+str(data['id'])
            else:
                sqlQuery="insert into platforms values('"+strdatetime+"',"+str(loginId)+", '"+str(data['coingeckoPlatformId'])+"', '"+str(data['name'])+"', "+str(data['shortname'])+", "+str(data['chainIdentifier'])+",null,null,0,null,null,1 )"
            output=Database.insertData(sqlQuery)
            if(output!="200"):
                    return Return.returnResponse("Some Internal Issue Occured While Saving. ",201)
            return Return.returnResponse("Platform Saved successfully. ",200)    
        
        else:
            return Return.returnResponse("Invalid url ",201) 

               
class UpdatePlatformData(MethodResource,Resource):
    '''
    This API is used to save Platform
    '''
    @handleException
    @doc(tags=['Platforms'], description=" save Platform API.")
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
            link="https://api.coingecko.com/api/v3/asset_platforms"
            res=requests.get(link)
            dataObj=json.loads(json.dumps(res.json()))
            if(dataObj==[]):
                return Return.returnResponse("Unable to fetch the platforms",201)

            for data in dataObj:
                if(data['chain_identifier']==None):
                    data['chain_identifier']='null'
                if(data['shortname']==None or data['shortname']==""):
                    data['shortname']='null'
                else :
                    data['shortname']="'"+data['shortname']+"'"
                q="select count(*) from platforms where coingecko_platform_id='"+str(data['id'])+"' "
                dataCount=Database.getValue(q)
                if(dataCount>0):
                    sqlQuery="update platforms set name='"+str(data['name'])+"', shortname="+str(data['shortname'])+", chain_identifier="+str(data['chain_identifier'])+"  where coingecko_platform_id='"+str(data['id'])+"'"
                else:
                    sqlQuery="insert into platforms values ('"+strdatetime+"',"+str(loginId)+",'"+str(data['id'])+"','"+str(data['name'])+"',"+str(data['shortname'])+", "+str(data['chain_identifier'])+", null, null,0,null,null,1)"
                output=Database.insertData(sqlQuery)
                if(output!="200"):
                    return Return.returnResponse("Some Internal Issue Occured While Saving. ",201)
            return Return.returnResponse("Platform Updated successfully. ",200) 
        else:
            return Return.returnResponse("Invalid url ",201)



class GetPlatformList(MethodResource,Resource):
    '''
    This API is used to get Platforms
    '''
    @handleException
    @doc(tags=['Platforms'], description=" save Platform API.")
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
            data=req.parse_args()
            if(loginAs==Constant.ADMINUSER):
                platformList=func.getPlatformsList(data['id'],flag=1)
            else:
                platformList=func.getPlatformsList(data['id'])
            return Return.returnResponse(platformList,200)
        else:
            return Return.returnResponse("Invalid URL ",201)


    
        
class DisableEnablePlatform(MethodResource,Resource):
    '''
    This API is used to Disable Enable Platform
    '''
    @handleException
    @doc(tags=['Platforms'], description=" Disable/Enable Platform API.")
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

        if(methodName=="disablePlatform" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update platforms set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Platform disable successfully.",200)
        elif(methodName=="enablePlatform" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update platforms set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Platform enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)


    
class DeletePlatform(MethodResource,Resource):
    '''
    This API is used to delete Platform
    '''
    @handleException
    @doc(tags=['Platforms'], description=" Delete Platform API.")
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
            query="update platforms set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            
            query1="select count(*) from cryptocurrency_platform_mapping where platform_id="+str(data['id'])
            datacount1=Database.getValue(query1)
            if(datacount1=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount1>0):
                sqlQuery1="update cryptocurrency_platform_mapping set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where platform_id="+str(data['id'])+""
                output1=Database.insertData(sqlQuery1)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Platform deleted successfully.",200)

        else:
            return Return.returnResponse("Invaild URL ",201)


            
class PermanentDeletePlatform(MethodResource,Resource):
    '''
    This API is used to delete Platform
    '''
    @handleException
    @doc(tags=['Platforms'], description=" Permanent Delete Platform API.")
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

            query1="select count(*) from cryptocurrency_platform_mapping where platform_id="+str(data['id'])+""
            datacount1=Database.getValue(query1)
            if(datacount1=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount1>0):
                sqlQuery1="delete cryptocurrency_platform_mapping where platform_id="+str(data['id'])+""
                output1=Database.insertData(sqlQuery1)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while deleting.",201)
                
            sqlquery1="delete platforms where id="+str(data['id'])+""
            output1=Database.insertData(sqlQuery1)
            if(output1!="200"):
                return Return.returnResponse("Some internal issue Occured while deleting.",201)
            return Return.returnResponse("Platform hard delete successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)


