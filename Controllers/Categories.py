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
from BAL.BALCategories import *

import time



class SaveCategory(MethodResource,Resource):
    '''
    This API is used to save Admin user
    '''
    @handleException
    @doc(tags=['Category'], description=" save Category API.")
    @use_kwargs(SaveCategorySchema,location=('json'))
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
            req.add_argument('coingeckoCategoryId',type=str,default=None,required=True,help="Please enter coingeckoCategoryId.")
            req.add_argument('name',type=str,default=None,required=True,help="Please enter name.")
            req.add_argument('link',type=str,default=None,required=False,help="Please enter link.")
            data=req.parse_args()

            if(link==None):
                data['link']='null'
            else:
                data[link]="'"+data['link']+"'"

            if(data['id']!=None):
                sqlQuery="update categories set coingecko_category_id='"+str(data['coingeckoCategoryId'])+"', name='"+str(data['name'])+"', link="+str(data['link'])+" where id="+str(data['id'])
            else:
                sqlQuery="insert into categories values('"+strdatetime+"',"+str(loginId)+", '"+str(data['coingeckoCategoryId'])+"', '"+str(data['name'])+"', "+str(data['link'])+", null,null,0,null,null,1 )"
            output=Database.insertData(sqlQuery)
            if(output!="200"):
                    return Return.returnResponse("Some Internal Issue Occured While Saving. ",201)
            return Return.returnResponse("Categories Saved successfully. ",200)  
        else:
            return Return.returnResponse("Invalid url. Please try again.",201)


class UpdateCategories(MethodResource,Resource):
    '''
    This API is used to update Category
    '''
    @handleException
    @doc(tags=['Category'], description=" Update Database Category API.")
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
            link="https://api.coingecko.com/api/v3/coins/categories/list"
            res=requests.get(link)
            if(res.status_code!=200):
                return Return.returnResponse("Some Internal Issue Occured While fetching. ",201)
            dataObj=json.loads(json.dumps(res.json()))
            if(dataObj==[]):
                return Return.returnResponse("Unable to fetch the categories",201)
            for data in dataObj:
                q="select count(*) from categories where coingecko_category_id='"+str(data['category_id'])+"'"
                dataCount=Database.getValue(q)
                if(dataCount>0):
                    sqlQuery="update platforms set name='"+data['name']+"' where coingecko_category_id='"+str(data['category_id'])+"'"
                else:
                    sqlQuery="insert into platforms values ('"+strdatetime+"', "+str(loginId)+",'"+str(data['id'])+"','"+str(data['name'])+"','"+str(data['shortname'])+"',"+str(data['chain_identifier'])+" null, null, 0,null,null,1)"
                output=Database.insertData(sqlQuery)
                if(output!="200"):
                    return Return.returnResponse("Some Internal Issue Occured While Saving. ",201)
            return Return.returnResponse("Platform Updated successfully. ",201) 
        else:
            return Return.returnResponse("Invalid url ",201) 



class GetCategoryList(MethodResource,Resource):
    '''
    This API is used to save Category
    '''
    @handleException
    @doc(tags=['Category'], description=" Update Database Category API.")
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
        if(loginAs==Constant.ADMINUSER or loginAs==Constant.CUSTOMER):
            req.add_argument('id',type=int,default=None,required=False)
            data=req.parse_args()
            func=BALCategories()
            if(loginAs==Constant.ADMINUSER):
                categoryList=func.getCategoriesList(data['id'],flag=1)
            else:
                categoryList=func.getCategoriesList(data['id'])
            return Return.returnResponse(categoryList,200)
        else:
            return Return.returnResponse("Invalid url ",201)




class DisableEnableCategory(MethodResource,Resource):
    '''
    This API is used to save Category
    '''
    @handleException
    @doc(tags=['Category'], description=" disableCategory/enableCategory API.")
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
        if(methodName=="disableCategory" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update categories set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Categories disable successfully.",200)
        elif(methodName=="enableCategory" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update categories set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Categories enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)




class DeleteCategory(MethodResource,Resource):
    '''
    This API is used to save Category
    '''
    @handleException
    @doc(tags=['Category'], description=" Delete Category API.")
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
            query="update categories set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            
            query1="select count(*) from cryptocurrency_category_mapping where platform_id="+str(data['id'])
            datacount1=Database.getValue(query1)
            if(datacount1=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount1>0):
                sqlQuery1="update cryptocurrency_category_mapping set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where platform_id="+str(data['id'])+""
                output1=Database.insertData(sqlQuery1)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Category deleted successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)


class PermanentDeleteCategory(MethodResource,Resource):
    '''
    This API is used to save Category
    '''
    @handleException
    @doc(tags=['Category'], description=" Permanently Delete Category API.")
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

            query1="select count(*) from cryptocurrency_category_mapping where platform_id="+str(data['id'])+""
            datacount1=Database.getValue(query1)
            if(datacount1=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount1>0):
                sqlQuery1="delete cryptocurrency_category_mapping where platform_id="+str(data['id'])+""
                output1=Database.insertData(sqlQuery1)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while deleting.",201)
                
            sqlquery1="delete categories where id="+str(data['id'])+""
            output1=Database.insertData(sqlQuery1)
            if(output1!="200"):
                return Return.returnResponse("Some internal issue Occured while deleting.",201)
            return Return.returnResponse("Category hard delete successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)

