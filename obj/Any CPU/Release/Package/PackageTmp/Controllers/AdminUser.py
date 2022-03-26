from flask_restful import Resource, reqparse
from datetime import datetime
from flask import Flask, Response , json ,request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from Models.ApiException import handleException
from Models.Schema import *
from Models.Function import *
from Models.Bean import *
from BAL.BALAdminusers import BALAdminusers

import time


class SaveAdminUser(MethodResource,Resource):
    '''
    This API is used to save Admin user
    '''
    @handleException
    @doc(tags=['AdminUser'], description=" save API.")
    @use_kwargs(SaveAdminUserSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers'))
    def post(self, **kwargs):
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        if(loginAs=="adminuser"):
            req.add_argument('id',type=int,default=None,required=False)
            req.add_argument('name',type=str,default=None,required=True,help='Please enter username field')
            req.add_argument('mobile',type=str,default=None,required=True,help='Please enter mobile field')
            req.add_argument('email',type=str,default=None,required=True,help='Please enter email field')
            req.add_argument('password',type=str,default=None,required=False,help='Please enter password field')
            data=req.parse_args()
            if(data['id']!=None):
                query="update admin_users set name='"+data['name']+"', email='"+data['email']+"', mobile='"+data['mobile']+"' where id="+str(data['id'])+" and deleted=0 and status=1"
            else :
                query ="insert into admin_users values('"+strdatetime+"', "+str(loginId)+", '"+data['name']+"', '"+data['mobile']+"', '"+data['email']+"', '"+data['password']+"', null,0,null,null,1)"
            output=Database.insertData(query)

            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured while saving data ",201)

            return Return.returnResponse("Admin User saved Successfully",200)
        else:
            return Return.returnResponse("Invalid url. Please try again.",201)


class GetAdminUserList(MethodResource,Resource):
    '''
    This API is used to get List Admin user
    '''
    @handleException
    @doc(tags=['AdminUser'], description=" getAdminUserList API.")
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
        if(loginAs=="adminuser"):
            req.add_argument('id',type=int,default=None)
            data=req.parse_args()
            func=BALAdminusers()
            adminUserslist=func.getAdminUsersList(data['id'],flag=1)
            return Return.returnResponse(adminUserslist,200)
        else:
            return Return.returnResponse("Invalid url. Please try again.",201)

class DisableEnableAdminUser(MethodResource,Resource):
    '''
    This API is used to update status field in database of the Adminuser
    '''
    @handleException
    @doc(tags=['AdminUser'], description="disable and enable API")
    @use_kwargs(IdSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers')) 
    def post(self, **kwargs):
        methodName=Function.getEndpoint(request.base_url)
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        if(methodName=="disable" and loginAs=="adminuser" ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update admin_users set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Adminuser disable successfully.",200)
        elif(methodName=="enable" and loginAs=="adminuser" ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update admin_users set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Adminuser enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)

class DeleteAdminUser(MethodResource,Resource):
    '''
    This API is used soft delete Admin user
    '''
    @handleException
    @doc(tags=['AdminUser'], description=" delete API")
    @use_kwargs(IdSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers')) 
    def delete(self, **kwargs):
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        if(loginAs=="adminuser"):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update admin_users set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Admin deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)


class LoginAdminUser(MethodResource,Resource):
    '''
    This API is used to login for Admin user
    '''
    @handleException
    @doc(tags=['AdminUser'], description="login API")
    @use_kwargs(loginSchema,location=('json'))
    def post(self, **kwargs):
        req=reqparse.RequestParser()
        strdatetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        req.add_argument('username',type=str,default=None,required=True,help='Please enter username field')
        req.add_argument('password',type=str,default=None,required=True,help='Please enter password field')            
        data=req.parse_args()
        query="select id,name,mobile,email,status from admin_users where (mobile='"+data['username']+"' or email='"+data['username']+"') and password='"+data['password']+"' and deleted=0 and status=1"
        cursor=Database.getCursor(query)
        if(cursor=="201"):
            return Return.returnResponse("Some Internal Issue Occured while saving data ",201)
        if(cursor==[]):
            return Return.returnResponse("No User Registered with this Username. Please try again.",201)
        adminUser=AdminModel()
        adminUser.id=cursor[0][0]
        adminUser.name=cursor[0][1]
        adminUser.mobile=cursor[0][2]
        adminUser.email=cursor[0][3]
        adminUser.status=cursor[0][4]

        Token=Function.createToken("adminuser",adminUser.id)
        if(Token=="201"):
            return Return.returnResponse("Some Internal Issue Occured. Please try again.",201)

        response=make_response( jsonify(
            {"Obj": json.loads(json.dumps(adminUser.__dict__))}
        ),
        200)
        response.headers["token"]=Token
        return response