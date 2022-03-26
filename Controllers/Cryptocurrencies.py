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
from BAL.BALCryptocurrencies import *
import time
import requests


class SaveCryptocurrency(MethodResource,Resource):
    '''
    This API is used to save Cryptocurrency
    '''
    @handleException
    @doc(tags=['Cryptocurrency'], description=" save Cryptocurrency API.")
    @use_kwargs(SaveCryptocurrencySchema,location=('json'))
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
            req.add_argument('coingeckoCryptoId',type=str,default=None,required=True,help='Please enter coingeckoCryptoId.')
            req.add_argument('name',type=str,default=None,required=True,help='Please enter name ')
            req.add_argument('symbol',type=str,default=None,required=True,help='Please enter symbol ')
            req.add_argument('image',type=str,default=None,required=False)
            req.add_argument('website',type=str,default=None,required=False)
            req.add_argument('sourceCode',type=str,default=None,required=False)
            req.add_argument('marketCap',type=float,default=None,required=False)
            req.add_argument('marketCapRank',type=float,default=None,required=False)
            req.add_argument('fullyDilutedValuation',type=float,default=None,required=False)
            req.add_argument('totalVolume',type=float,default=None,required=False)
            req.add_argument('circulatingSupply',type=float,default=None,required=False)
            req.add_argument('totalSuppy',type=float,default=None,required=False)
            req.add_argument('maxSupply',type=float,default=None,required=False)
            req.add_argument('ath',type=float,default=None,required=False)
            req.add_argument('athChangePercentage',type=float,default=None,required=False)
            req.add_argument('athDate',type=str,default=None,required=False)
            req.add_argument('atl',type=float,default=None,required=False)
            req.add_argument('atlChangePercentage',type=float,default=None,required=False)
            req.add_argument('atlDate',type=str,default=None,required=False)
            req.add_argument('roi',type=float,default=None,required=False)
            data=req.parse_args()
            qname=Function.checkSingleQuote(data['name'])

            q="select count(*) from cryptocurrencies where coingecko_crypto_id='"+data['coingeckoCryptoId']+"' and deleted=0 and status=1"        
            dataCount=Database.getValue(q)
            if(dataCount=="201"):
                return Return.returnResponse("Some Internal Issue Occured while saving data ",201)
            if(dataCount>0):
                sqlQuery="update cryptocurrencies set name='"+qname+"', symbol='"+data['symbol']+"', image='"+data['image']+"', market_cap="+str(data['marketCap'])+" ,market_cap_rank="+str(data['marketCapRank'])+" , fully_diluted_valuation= "+str(data['fullyDilutedValuation'])+" , total_volume="+str(data['totalVolume'])+" , circulating_supply="+str(data['circulatingSupply'])+" ,total_supply="+str(data['total_supply'])+",max_supply="+str(data['maxSupply'])+" ,ath= "+str(data['ath'])+", ath_change_percentage="+str(data['athChangePercentage'])+", ath_date="+str(data['athDate'])+", atl="+str(data['atl'])+" , atl_change_percentage="+str(data['atlChangePercentage'])+" , atl_date="+data['atlDate']+", roi="+str(roi_percentage)+", last_updated='"+strdatetime+"' where coingecko_crypto_id='"+data['coingeckoCryptoId']+"'"
            else:
                sqlQuery="insert into cryptocurrencies values ('"+strdatetime+"', 8, '"+data['coingeckoCategoryId']+"', '"+qname+"', '"+data['symbol']+"', '"+data['image']+"',null ,null , "+str(data['marketCap'])+", "+str(data['marketCapRank'])+", "+str(data['fullyDilutedValuation'])+", "+str(data['totalVolume'])+", "+str(data['circulatingSupply'])+", "+str(data['totalSupply'])+", "+str(data['maxSupply'])+", "+str(data['ath'])+", "+str(data['athChangePercentage'])+", "+str(data['athDate'])+", "+str(data['atl'])+", "+str(data['atlChangePercentage'])+", "+data['atlDate']+", "+str('roi')+", '"+strdatetime+"',null,null,null,null, 0,null,null,1)"
                           
            if(output!="200"):
                return Return.returnResponse("Some Internal Issue Occured while saving data ",201)

            return Return.returnResponse("Cryptocurrency saved Successfully",200)
        else:
            return Return.returnResponse("Invalid url ",201)


class UpdateCryptocurrencyData(MethodResource,Resource):
    '''
    This API is used to save Cryptocurrency
    '''
    @handleException
    @doc(tags=['Cryptocurrency'], description=" Update Cryptocurrency Data API.")
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
            func=Function()
            func.updateDatabase()
            return Return.returnResponse("Cryptocurrency data updated successfully",200)
        else:
            return Return.returnResponse("Invalid url ",201)


class UpdateCryptocurrencyDetails(MethodResource,Resource):
    '''
    This API is used to save Cryptocurrency
    '''
    @handleException
    @doc(tags=['Cryptocurrency'], description=" Update Cryptocurrency Details API.(This might take some time)")
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
            sqlQuery="select id, coingecko_crypto_id from cryptocurrencies where deleted=0 and status=1 "
            data=Database.getCursor(sqlQuery)
            if(data!="201" and data!=[]):
                for row in data:
                    #print(time.ctime())
                    time.sleep(0.5)
                    print(row[0])
                    link="https://api.coingecko.com/api/v3/coins/"+str(row[1])
                    res=requests.get(link)
                    if(res.status_code!=200):
                        continue
                    resObj=json.loads(json.dumps(res.json()))   
                    if(resObj==[]):
                        continue    
                    setQuery=""
                    if(len(resObj['links']['homepage'])>0):
                        if(resObj['links']['homepage'][0]!="" and resObj['links']['homepage'][0]!=None):
                            setQuery=" website='"+str(resObj['links']['homepage'][0])+"' ,"    
                    if(len(resObj['links']['repos_url']['github'])>0):
                        if(resObj['links']['repos_url']['github'][0]!="" and resObj['links']['repos_url']['github'][0]!=None):
                            setQuery=setQuery+" source_code='"+str(resObj['links']['repos_url']['github'][0])+"' ,"
                    if(len(setQuery)>0):                
                        query1="update cryptocurrencies set "+str(setQuery[:len(setQuery)-1])+" where id="+str(row[0])+" "
                        output1=Database.insertData(query1)
                        if(output1=="201"):
                            return Return.returnResponse("Some internal issue occured while saving data.",201)

                    if(resObj['links']['subreddit_url']!="" and resObj['links']['subreddit_url']!=None):
                        q1="select count(*) from community where cryptocurrency_id="+str(row[0])+" and name='Reddit' and link='"+str(resObj['links']['subreddit_url'])+"'"
                        datacount1=Database.getValue(q1)
                        if(datacount1=='201'):
                            return Return.returnResponse("Some internal issue occured while saving data. ",201)
                        if(datacount1>0 ):
                            query2="update community set cryptocurrency_id="+str(row[0])+" name='Reddit' and link='"+str(resObj['links']['subreddit_url'])+"' "
                        else:
                            query2="insert into community values('"+strdatetime+"',8,"+str(row[0])+",'Reddit','"+str(resObj['links']['subreddit_url'])+"',null,null,null,0,null,null,1)"
                        output2=Database.insertData(query2)
                        if(output2=="201"):
                            return Return.returnResponse("Some internal issue occured while saving data.",201)
                    if(resObj['links']['facebook_username']!="" and resObj['links']['facebook_username']!=None):
                        q2="select count(*) from community where cryptocurrency_id="+str(row[0])+" and name='Facebook' and link='https://www.facebook.com/"+str(resObj['links']['facebook_username'])+"/'"
                        datacount2=Database.getValue(q2)
                        if(datacount2=='201'):
                            return Return.returnResponse("Some internal issue occured while saving data. ",201)
                        if(datacount2>0 ):
                            query3="update community set cryptocurrency_id="+str(row[0])+" name='Facebook' and link='https://www.facebook.com/"+str(resObj['links']['facebook_username'])+"/' "
                        else:
                            query3="insert into community values('"+strdatetime+"',8,"+str(row[0])+",'Facebook','https://www.facebook.com/"+str(resObj['links']['facebook_username'])+"/',null,null,null,0,null,null,1)"
                        output3=Database.insertData(query3)
                        if(output3=="201"):
                            return Return.returnResponse("Some internal issue occured while saving data.",201)
                    if(resObj['links']['twitter_screen_name']!="" and resObj['links']['twitter_screen_name']!=None):
                        q2="select count(*) from community where cryptocurrency_id="+str(row[0])+" and name='Twitter' and link='https://twitter.com/"+str(resObj['links']['twitter_screen_name'])+"'"
                        datacount3=Database.getValue(q2)
                        if(datacount3=='201'):
                            return Return.returnResponse("Some internal issue occured while saving data. ",201)
                        if(datacount3>0 ):
                            query4="update community set cryptocurrency_id="+str(row[0])+" name='Twitter' and link='https://twitter.com/"+str(resObj['links']['twitter_screen_name'])+"' "
                        else:
                            query4="insert into community values('"+strdatetime+"',8,"+str(row[0])+",'Twitter','https://twitter.com/"+str(resObj['links']['twitter_screen_name'])+"',null,null,null,0,null,null,1)"
                        output2=Database.insertData(query4)
                        if(output2=="201"):
                            return Return.returnResponse("Some internal issue occured while saving data.",201)
                    if(resObj['links']['telegram_channel_identifier']!="" and resObj['links']['telegram_channel_identifier']!=None):
                        q4="select count(*) from community where cryptocurrency_id="+str(row[0])+" and name='Telegram' and link='"+str(resObj['links']['telegram_channel_identifier'])+"'"
                        datacount4=Database.getValue(q4)
                        if(datacount4=='201'):
                            return Return.returnResponse("Some internal issue occured while saving data. ",201)
                        if(datacount4>0 ):
                            query5="update community set cryptocurrency_id="+str(row[0])+" name='Telegram' and link='https://t.me/"+str(resObj['links']['telegram_channel_identifier'])+"' "
                        else:
                            query5="insert into community values('"+strdatetime+"',8,"+str(row[0])+",'Telegram','https://t.me/"+str(resObj['links']['telegram_channel_identifier'])+"',null,null,null,0,null,null,1)"
                        output2=Database.insertData(query5)
                        if(output2=="201"):
                            return Return.returnResponse("Some internal issue occured while saving data.",201)
                    
                    if(len(resObj['categories'])>0 and resObj['categories']!=[]):
                        for category in resObj['categories']:
                            if(category!="" and category!=None):
                                query6="select id, name from categories where name ='"+str(category)+"'"
                                categoryData=Database.getCursor(query6)
                                if(categoryData!="201" and categoryData!=[]):
                                    q5="select count(*) from cryptocurrency_category_mapping where category_id="+str(categoryData[0][0])+" and cryptocurrency_id="+str(row[0])+" "
                                    datacount5=Database.getValue(q5)
                                    if(datacount5=='201'):
                                        return Return.returnResponse("Some internal issue occured while saving data. ",201)
                                    if(datacount5==0 ):
                                        query5="insert into cryptocurrency_category_mapping values('"+strdatetime+"',8,"+str(row[0])+","+str(categoryData[0][0])+",null,0,null,null,1)"
                                        output2=Database.insertData(query5)
                                        if(output2=="201"):
                                            return Return.returnResponse("Some internal issue occured while saving data.",201)

                    if(len(resObj['links']['blockchain_site'])>0 and resObj['links']['blockchain_site']!=[]):
                        for site in resObj['links']['blockchain_site']:
                            if(site!="" and site!=None):
                                q6="select count(*) from explorers where cryptocurrency_id="+str(row[0])+" and link='"+str(site)+"'"
                                datacount6=Database.getValue(q6)
                                if(datacount6=='201'):
                                    return Return.returnResponse("Some internal issue occured while saving data. ",201)
                                if(datacount6==0 ):
                                    query6="insert into explorers values('"+strdatetime+"',8,"+str(row[0])+",null,'"+str(site)+"',null,null,0,null,null,1)"
                                    output2=Database.insertData(query6)
                                    if(output2=="201"):
                                        return Return.returnResponse("Some internal issue occured while saving data.",201)
                    if(len(resObj['platforms'])>0):
                        for coingeckoPlatformId, contractAddress in resObj['platforms'].items():
                            if(contractAddress==None):
                                contractAddress="null"
                            else :
                                contractAddress="'"+str(contractAddress)+"'"
                            if(coingeckoPlatformId!=None and coingeckoPlatformId!=""):
                                q7="select id from platforms where coingecko_platform_id='"+str(coingeckoPlatformId)+"'"
                                platformId=Database.getValue(q7)
                                if(platformId==None):
                                    quert7="insert into platforms values('"+str(strdatetime)+"',"+str(loginId)+",'"+coingeckoPlatformId+"',null,null,null,0,null,null,1)"
                                    output6=Database.insertData(query7)
                                    if(output6=="201"):
                                        return Return.returnResponse("Some internal issue occured while saving data.",201)
                                    q7="select id from platforms where coingecko_platform_id='"+str(platformId)+"'"
                                    platformId=Database.getValue(q7)
                                q8="select count(*) from cryptocurrency_platform_mapping where cryptocurrency_id="+str(row[0])+" and platform_id= "+str(platformId)+""
                                datacount7=Database.getValue(q8)
                                if(datacount7=='201'):
                                    return Return.returnResponse("Some internal issue occured while saving data. ",201)
                                if (datacount7>0):
                                    query8="update cryptocurrency_platform_mapping set contract_address="+str(contractAddress)+" where cryptocurrency_id="+str(row[0])+" and platform_id="+str(platformId)+""
                                else:   
                                    query8="insert into cryptocurrency_platform_mapping values('"+str(strdatetime)+"',"+str(loginId)+","+str(row[0])+","+str(platformId)+","+contractAddress+",0,null,null,1)"
                                output7=Database.insertData(query8)
                                if(output7=="201"):
                                    return Return.returnResponse("Some internal issue occured while saving data.",201)
            return Return.returnResponse("Cryptocurrency Details updated Successfully.",200)
        else:
            return Return.returnResponse("Invalid url ",201)


class GetCryptocurrencyList(MethodResource,Resource):
    '''
    This API is used to get Cryptocurrency list
    '''
    @handleException
    @doc(tags=['Cryptocurrency'], description=" Get Cryptocurrency List API.")
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

        req.add_argument('id',type=int,default=None,required=False)
        data=req.parse_args()
        func=BALCryptocurrencies()
        if(loginAs=="adminuser"):
            cryptocurrenciesList=func.getCryptocurrenciesList(data['id'],flag=1)
        else:
            cryptocurrenciesList=func.getCryptocurrenciesList(data['id'])
        return Return.returnResponse(cryptocurrenciesList,200)


class DisableEnableCryptocurrency(MethodResource,Resource):
    '''
    This API is used to Disable/Enable Cryptocurrency
    '''
    @handleException
    @doc(tags=['Cryptocurrency'], description=" Disable/Enable Cryptocurrency API.")
    @use_kwargs(SaveCryptocurrencySchema,location=('json'))
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
        if(methodName=="disableCryptocurrency" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurencies set status=0 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Cryptocurency disable successfully.",200)
        elif(methodName=="enableCryptocurency" and loginAs==Constant.ADMINUSER ):
            req.add_argument('id',type=int,default=None,required=True,help='Invalid Login.')
            data=req.parse_args()
            query="update cryptocurencies set status=1 where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output=="201"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            return Return.returnResponse("Cryptocurency enable successfully.",200)
        
        else:                   
            return Return.returnResponse("Invalid url ",201)

       
class DeleteCryptocurrency(MethodResource,Resource):
    '''
    This API is used to delete Cryptocurrency
    '''
    @handleException
    @doc(tags=['Cryptocurrency'], description=" delete Cryptocurrency API.")
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
            query="update cryptocurrencies set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)
            
            query1="select count(*) from community where cryptocurrency_id="+str(data['id'])
            datacount1=Database.getValue(query1)
            if(datacount1=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount1>0):
                sqlQuery1="update community set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where cryptocurrency_id="+str(data['id'])+""
                output1=Database.insertData(sqlQuery1)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query2="select count(*) from cryptocurrency_category_mapping where cryptocurrency_id="+str(data['id'])
            datacount2=Database.getValue(query2)
            if(datacount2=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount2>0):
                sqlQuery2="update cryptocurrency_category_mapping set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where cryptocurrency_id="+str(data['id'])+""
                output2=Database.insertData(sqlQuery2)
                if(output2!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query3="select count(*) from cryptocurrency_platform_mapping where cryptocurrency_id="+str(data['id'])
            datacount3=Database.getValue(query3)
            if(datacount3=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount3>0):
                sqlQuery3="update cryptocurrency_platform_mapping set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where cryptocurrency_id="+str(data['id'])+""
                output3=Database.insertData(sqlQuery3)
                if(output3!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query4="select count(*) from cryptocurrency_history where cryptocurrency_id="+str(data['id'])
            datacount4=Database.getValue(query4)
            if(datacount4=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount4>0):
                sqlQuery4="update cryptocurrency_history set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where cryptocurrency_id="+str(data['id'])+""
                output4=Database.insertData(sqlQuery4)
                if(output4!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query5="select count(*) from explorers where cryptocurrency_id="+str(data['id'])
            datacount5=Database.getValue(query5)
            if(datacount5=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount5>0):
                sqlQuery5="update explorers set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where cryptocurrency_id="+str(data['id'])+""
                output5=Database.insertData(sqlQuery5)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query6="select count(*) from watch_list where cryptocurrency_id="+str(data['id'])
            datacount6=Database.getValue(query6)
            if(datacount6=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount6>0):
                sqlQuery6="update watch_list set deleted=1, deleted_by_id="+str(loginId)+", deleted_timestamp='"+str(strdatetime)+"' where cryptocurrency_id="+str(data['id'])+""
                output6=Database.insertData(sqlQuery6)
                if(output6!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)
         
            return Return.returnResponse("Cryptocurency deleted successfully.",200)
        else:                   
            return Return.returnResponse("Invalid url ",201)

               
class PermanentDeleteCryptocurrency(MethodResource,Resource):
    '''
    This API is used to Permanent delete Cryptocurrency
    '''
    @handleException
    @doc(tags=['Cryptocurrency'], description="Permanent delete Cryptocurrency API.")
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
            
            query1="select count(*) from community where cryptocurrency_id="+str(data['id'])
            datacount1=Database.getValue(query1)
            if(datacount1=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount1>0):
                sqlQuery1="delete community where cryptocurrency_id="+str(data['id'])+""
                output1=Database.insertData(sqlQuery1)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query2="select count(*) from cryptocurrency_category_mapping where cryptocurrency_id="+str(data['id'])
            datacount2=Database.getValue(query2)
            if(datacount2=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount2>0):
                sqlQuery2="delete cryptocurrency_category_mapping where cryptocurrency_id="+str(data['id'])+""
                output2=Database.insertData(sqlQuery2)
                if(output2!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query3="select count(*) from cryptocurrency_platform_mapping where cryptocurrency_id="+str(data['id'])
            datacount3=Database.getValue(query3)
            if(datacount3=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount3>0):
                sqlQuery3="delete cryptocurrency_platform_mapping where cryptocurrency_id="+str(data['id'])+""
                output3=Database.insertData(sqlQuery3)
                if(output3!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query4="select count(*) from cryptocurrency_history where cryptocurrency_id="+str(data['id'])
            datacount4=Database.getValue(query4)
            if(datacount4=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount4>0):
                sqlQuery4="delete cryptocurrency_history where cryptocurrency_id="+str(data['id'])+""
                output4=Database.insertData(sqlQuery4)
                if(output4!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query5="select count(*) from explorers where cryptocurrency_id="+str(data['id'])
            datacount5=Database.getValue(query5)
            if(datacount5=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount5>0):
                sqlQuery5="delete explorers where cryptocurrency_id="+str(data['id'])+""
                output5=Database.insertData(sqlQuery5)
                if(output1!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query6="select count(*) from watch_list where cryptocurrency_id="+str(data['id'])
            datacount6=Database.getValue(query6)
            if(datacount6=="201"):
                return Return.returnResponse("Some internal issue Occured while fetching.",201)
            if(datacount6>0):
                sqlQuery6="delete watch_list where cryptocurrency_id="+str(data['id'])+""
                output6=Database.insertData(sqlQuery6)
                if(output6!="200"):
                    return Return.returnResponse("Some internal issue Occured while updating.",201)

            query="delete cryptocurrencies where id="+str(data['id'])+""
            output=Database.insertData(query)
            if(output!="200"):
                return Return.returnResponse("Some internal issue Occured while updating.",201)

            return Return.returnResponse("Cryptocurency hard delete successfully.",200)
        else:
            return Return.returnResponse("Invalid URL ",201)
