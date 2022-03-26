from flask_restful import Resource, reqparse
from datetime import datetime
from flask import Flask, Response , json ,request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from Models.ApiException import handleException
from Models.Schema import *
from Models.Function import *
from Models.Bean import *
from BAL.BALCustomers import BALCustomers
from Models.Constant import *
import time


class SaveCustomer(MethodResource,Resource):
    
    '''
    This API is used to save Customer
    '''
    @handleException
    @doc(tags=['Customers'], description="saveCustomer API")
    @use_kwargs(SaveCustomersSchema,location=('json'))
    @use_kwargs(TokenSchema,location=('headers'))
    def post(self, **kwargs):
        loginObj=Function.verifyToken()
        if(isinstance(loginObj,str)):
            return Return.returnResponse(loginObj,201)
        loginId=loginObj[0]
        loginAs=loginObj[1]
        req=reqparse.RequestParser()
        strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        req.add_argument('id',type=int,default=None,required=False)
        req.add_argument('name',type=str,default=None,required=True,help='Please enter username field')
        req.add_argument('mobile',type=str,default=None,required=True,help='Please enter mobile field')
        req.add_argument('email',type=str,default=None,required=True,help='Please enter email field')
        req.add_argument('password',type=str,default=None,required=True,help='Please enter email field')
        data=req.parse_args()
        #current DateTime
        strdatetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if(data['id']!=None):
            query="update customers set name='"+data['name']+"', mobile='"+data['mobile']+"', email='"+data['email']+"' where id="+str(data['id'])+" and deleted=0 and status=1"
        else:
            query ="insert into customers values('"+strdatetime+"', 8, '"+data['name']+"', '"+data['mobile']+"', '"+data['email']+"', '"+data['password']+"',0,null,null,1)"
        output=Database.insertData(query)

        if(output!="200"):
            return Return.returnResponse("Some Internal Issue Occured while saving data ",201)

        return Return.returnResponse("customer saved Successfully",200)

    
class GetCustomerList(MethodResource,Resource):
    '''
    This API is used to get list of the customer
    '''
    @handleException
    @doc(tags=['Customers'], description="getCustomerList")
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
        if(loginAs==Constant.ADMINUSER or loginAs==Constant.CUSTOMER ):
            req.add_argument('id',type=int,default=None,required=False)
            data=req.parse_args()
            func=BALCustomers()
            if(loginAs=="adminuser"):
                customerList=func.getCustomersList(id=data['id'],flag=1)
            else:
                customerList=func.getCustomersList(loginId)
            return Return.returnResponse(customerList,200)
        else:
            return Return.returnResponse("Invaild URL ",201)


class DisableEnableCustomer(MethodResource,Resource):
    '''
    This API is used to update status field in database of the Customer
    '''
    @handleException
    @doc(tags=['Customers'], description="disableCustomer/enableCustomer API.")
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
        if(methodName=="disableCustomer" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update customers set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Customer disable successfully.",200)
        elif(methodName=="enableCustomer" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update customers set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",200)
            return Return.returnResponse("Customer enable successfully.",200)
        else:
            return Return.returnResponse("Invaild URL ",201)

class DeleteCustomer(MethodResource,Resource):
    '''
    This API is used to soft delete of the Customer
    '''
    @handleException
    @doc(tags=['Customers'], description="delete API.")
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
        if( loginAs==Constant.ADMINUSER):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update customers set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Customer deleted successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)



class LoginCustomer(MethodResource,Resource):
    '''
    This API is used to login for Customer
    '''
    @handleException
    @doc(tags=['Customers'], description="login API")
    @use_kwargs(loginSchema,location=('json'))
    def post(self, **kwargs):
        req=reqparse.RequestParser()
        strdatetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        req.add_argument('username',type=str,default=None,required=True,help='Please enter email field')
        req.add_argument('password',type=str,default=None,required=True,help='Please enter password field')            
        data=req.parse_args()
        query="select id,name,mobile,email from customers where (mobile='"+data['username']+"' or email='"+data['username']+"') and password='"+data['password']+"' and deleted=0 and status=1 "
        cursor=Database.getCursor(query)
        if(cursor=="201" ):
            return Return.returnResponse("Some Internal Issue Occured while saving data ",201)
        if(cursor==[]):
            return Return.returnResponse("No User Registered. Please try again.",201)
        customer=CustomerModel()
        customer.id=cursor[0][0]
        customer.name=cursor[0][1]
        customer.mobile=cursor[0][2]
        customer.email=cursor[0][3]

        Token=Function.createToken("customer",customer.id)
        if(Token=="201"):
            return Return.returnResponse("Some Internal Issue Occured. Please try again.",201)

        response=make_response( jsonify(
            {"Obj": json.loads(json.dumps(customer.__dict__))}
        ),
        200)
        response.headers["token"]=Token
        return response
