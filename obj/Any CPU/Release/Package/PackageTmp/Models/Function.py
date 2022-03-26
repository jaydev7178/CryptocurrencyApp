from apscheduler.schedulers.background import BackgroundScheduler
from email import encoders
from flask_mail import Mail, Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dateutil.relativedelta import relativedelta
from flask import request
from datetime import datetime
from BAL.BALCustomers import *
from Models.Database import *
from Models.Return import *
from Models.Bean import TokenObject
import requests
import uuid
import jwt
import datetime as dt
import socket
import time


class Function:

    @staticmethod
    def createToken(loginAs, id):
        from Routes.app import app
        try:
            if(loginAs != None and id!= None):
                time =dt.datetime.now()+ relativedelta(months=+1)
                key=bytes(str(uuid.uuid4()),'utf-8')
                token=jwt.encode({'LoginAs':loginAs,'id':id,'VaildTill':str(time)},app.config['SECRET_KEY'],algorithm="HS256")
                return token
            else:
                return "Invaild Login"
        except Exception as e:
            return "201"

    @staticmethod
    def validateToken(token):
        from Routes.app import app
        try:
            if(token != None):
                jsonToken=jwt.api_jwt.decode_complete(token, app.config['SECRET_KEY'],algorithms="HS256")
                if(jsonToken['payload']['LoginAs']):
                    vaildate=str(jsonToken['payload']['VaildTill']).rsplit('.',1)
                    validTill=dt.datetime.strptime(vaildate[0],'%Y-%m-%d %H:%M:%S')
                    if(validTill>dt.datetime.now()):
                        return TokenObject(jsonToken['payload']['id'],jsonToken['payload']['LoginAs'])
                    else:
                        return "INVALID:LOGIN"
        except Exception as e:
            return "201"

    @staticmethod
    def verifyToken():
        from Models.JWTRequestFilter import JWTRequestFilter
        tokenObj=JWTRequestFilter.checkToken()
        if(isinstance(tokenObj,TokenObject)):
            loginId=tokenObj.id
            loginAs=tokenObj.loginAs
        elif(isinstance(tokenObj,str)):
            return tokenObj
        return loginId,loginAs

    @staticmethod
    def sendMail(sub=None,body=None,bcc=[],recipients=['jaydev@cuttingedgeinfotech.com']):
        try:
            if(sub==None or body==None or recipients==[]):
                return "201"
            from Routes.app import app
            app.config['MAIL_SERVER']='cuttingedgeinfotech.com'
            app.config['MAIL_PORT'] = 587
            app.config['MAIL_USERNAME'] = 'jaydev@cuttingedgeinfotech.com'
            app.config['MAIL_PASSWORD'] = 'js@2020#'
            app.config['MAIL_USE_TLS'] = False
            app.config['MAIL_USE_SSL'] = False
            mail = Mail(app)
            msg = Message(
                    subject=sub,
                    sender ='jaydev@cuttingedgeinfotech.com',
                    recipients = recipients,
                    bcc=bcc
                    )
            msg.body = body
            if(mail.connect):
                mail.send(msg)

        except Exception as e:
            return "201"
        return "200"

    @staticmethod
    def checkSingleQuote(strObj):
        if(strObj!=None):
            if(strObj.find("'") >= 0 ):
                strObj=strObj.replace("'","''")          
            return strObj
        else:
            return strObj

    @staticmethod
    def getEndpoint(base_url):
        methodName=base_url.rsplit("/",1)[1]
        if(methodName==None):
            return "201"
        return methodName

    @staticmethod
    def updateDatabase():
        strdatetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("schedule started at "+strdatetime)
        count =1
        func=BALCustomers()
        for count in range(1,1000):
            time.sleep(1)
            link="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page="+str(count)+"&sparkline=false&price_change_percentage=1h%2C24h%2C7d%2C14d%2C30d%2C200d%2C1y"
            #link="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=gecko_asc&per_page=250&page=90&sparkline=false"
            res=requests.get(link)
            if(res.status_code!=200):
                continue
            dataObj=json.loads(json.dumps(res.json()))
            if(dataObj==[]):
                break
            
            roi_percentage="null"
            #print("Page no. "+str(count))
            strdatetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            for data in dataObj:
                if(data['roi']!=None):
                    if(data['roi']['percentage']!=None):
                        roi_percentage=data['roi']['percentage']
                    else :
                        roi_percentage='null'
                qname=Function.checkSingleQuote(data['name'])
                if(data['last_updated']==None):
                    data['last_updated']=strdatetime
                if(data['ath_date']!=None):
                    data['ath_date']="'"+data['ath_date']+"'"
                if(data['atl_date']!=None):
                    data['atl_date']="'"+data['atl_date']+"'"
                if(data['symbol'].find('💲')>=0):
                    data['symbol']=data['symbol'].replace('💲','')

                for key in data:
                    if(data[key]==None and key!='roi'and key!='last_updated'):
                        data[key]='null'                     
                q="select count(*) from cryptocurrencies where coingecko_crypto_id='"+data['id']+"' and deleted=0 and status=1"        
                dataCount=Database.getValue(q)
                if(dataCount=="201"):
                    subject="ERROR in query"
                    msg="error occured in while fetching "+data['id']
                    recipients=['jaydev@cuttingedgeinfotech.com']
                    mailOutput=Function.sendMail(subject,msg ,None,recipients)
                    #return Return.returnResponse("Some Internal Issue Occured while saving data ",201)
                if(dataCount>0):
                    sqlQuery="update cryptocurrencies set name='"+qname+"', symbol='"+data['symbol']+"', image='"+data['image']+"', market_cap="+str(data['market_cap'])+" ,market_cap_rank="+str(data['market_cap_rank'])+" , fully_diluted_valuation= "+str(data['fully_diluted_valuation'])+" , total_volume="+str(data['total_volume'])+" , circulating_supply="+str(data['circulating_supply'])+" ,total_supply="+str(data['total_supply'])+",max_supply="+str(data['max_supply'])+" ,ath= "+str(data['ath'])+", ath_change_percentage="+str(data['ath_change_percentage'])+", ath_date="+str(data['ath_date'])+", atl="+str(data['atl'])+" , atl_change_percentage="+str(data['atl_change_percentage'])+" , atl_date="+data['atl_date']+", roi="+str(roi_percentage)+", last_updated='"+data['last_updated']+"' where coingecko_crypto_id='"+data['id']+"'"
                else:
                    sqlQuery="insert into cryptocurrencies values ('"+strdatetime+"', 8, '"+data['id']+"', '"+qname+"', '"+data['symbol']+"', '"+data['image']+"',null ,null , "+str(data['market_cap'])+", "+str(data['market_cap_rank'])+", "+str(data['fully_diluted_valuation'])+", "+str(data['total_volume'])+", "+str(data['circulating_supply'])+", "+str(data['total_supply'])+", "+str(data['max_supply'])+", "+str(data['ath'])+", "+str(data['ath_change_percentage'])+", "+str(data['ath_date'])+", "+str(data['atl'])+", "+str(data['atl_change_percentage'])+", "+data['atl_date']+", "+str(roi_percentage)+", '"+data['last_updated']+"',null,null,null,null, 0,null,null,1)"
                    subject="New Cryptocurrecy"
                    msg="New Cryptocurrency is available "+data['name']+" ("+data['symbol']+")"
                    bcc=[]
                    
                    bcc=func.getCustomerEmailList()
                    mailOutput=Function.sendMail(subject,msg,bcc)
                    #return Return.returnResponse("Some Internal Issue Occured while sending mail ",201)
                output=Database.insertData(sqlQuery)
                if(output!="200"):
                    subject="ERROR in updating Cryptocurrencies "
                    msg="Error "+output.value[1]+" occured in while executing query "+sqlQuery
                    recipients=['jaydev@cuttingedgeinfotech.com']
                    mailOutput=Function.sendMail(subject,msg ,None,recipients)
                    
                q1="select id from cryptocurrencies where coingecko_crypto_id='"+data['id']+"'"
                cryptocurrencyId=Database.getValue(q1)
                if(cryptocurrencyId!="201" and cryptocurrencyId!=None):
                    q2="select count(*) from cryptocurrency_history where cryptocurrency_id ="+str(cryptocurrencyId)+" and deleted=0 and status=1 "
                    dataCount1=Database.getValue(q2)
                    if(dataCount1>0):
                        sqlQueryHistory="update cryptocurrency_history set current_price= "+str(data['current_price'])+" ,high_24h= "+str(data['high_24h'])+"  , low_24h =  "+str(data['low_24h'])+" , price_change_24h=  "+str(data['price_change_24h'])+" ,market_cap_change_24h =  "+str(data['market_cap_change_24h'])+" , market_cap_change_percentage_24h=  "+str(data['market_cap_change_percentage_24h'])+" , price_change_percentage_1h_in_currency=  "+str(data['price_change_percentage_1h_in_currency'])+" , price_change_percentage_24h_in_currency=  "+str(data['price_change_percentage_24h_in_currency'])+" , price_change_percentage_7d_in_currency=  "+str(data['price_change_percentage_7d_in_currency'])+" , price_change_percentage_14d_in_currency=  "+str(data['price_change_percentage_7d_in_currency'])+" , price_change_percentage_30d_in_currency=  "+str(data['price_change_percentage_30d_in_currency'])+" , price_change_percentage_200d_in_currency=  "+str(data['price_change_percentage_200d_in_currency'])+" , price_change_percentage_1y_in_currency= "+str(data['price_change_percentage_1y_in_currency'])+" where cryptocurrency_id="+str(cryptocurrencyId)+" and deleted=0 and status=1"
                    else:
                        sqlQueryHistory="insert into cryptocurrency_history values('"+strdatetime+"', 8,"+str(cryptocurrencyId)+","+str(data['current_price'])+", "+str(data['high_24h'])+", "+str(data['low_24h'])+", "+str(data['price_change_24h'])+", "+str(data['market_cap_change_24h'])+", "+str(data['market_cap_change_percentage_24h'])+", "+str(data['price_change_percentage_1h_in_currency'])+", "+str(data['price_change_percentage_24h_in_currency'])+", "+str(data['price_change_percentage_7d_in_currency'])+", "+str(data['price_change_percentage_14d_in_currency'])+", "+str(data['price_change_percentage_30d_in_currency'])+", "+str(data['price_change_percentage_200d_in_currency'])+", "+str(data['price_change_percentage_1y_in_currency'])+", null,null,null, 0, null,null, 1)"   
                    output1=Database.insertData(sqlQueryHistory)
                    if(output1!="200"):
                        subject="ERROR in updating history"
                        msg="Error "+output.value[1]+" occured in while executing query "+sqlQuery
                        recipients=['jaydev@cuttingedgeinfotech.com']
                        mailOutput=Function.sendMail(subject,msg ,None,recipients)
                    
                    q3="select count(*) from watch_list where cryptocurrency_id="+str(cryptocurrencyId)+" and deleted=0 and status=1"
                    dataCount2=Database.getValue(q3)
                    if(dataCount2>0):
                        sqlQueryWatchList="select id, customer_id, min_threshold, max_threshold from watch_list where cryptocurrency_id="+str(cryptocurrencyId)+" and min_threshold <"+str(data['current_price'])+" or max_threshold > "+str(data['current_price'])+" and deleted=0 and status=1"
                        watchlistcursor=Database.getCursor(sqlQueryWatchList)
                        if(watchlistcursor!=None ):
                            for row in watchlistcursor:
                                customer=func.getCustomersList(row[1])
                                subject="Cryptocurrency alert "
                                recipients=[customer[0]['email']]                                
                                if(watchlistcursor[0][2]>data['current_price']):
                                    msg="The Price of "+data['name']+" ("+data['symbol']+") is decrease to "+str(data['current_price'])
                                elif(watchlistcursor[0][3]<data['current_price']):
                                    msg="The Price of "+data['name']+" ("+data['symbol']+") is increase to "+str(data['current_price'])
                                mailOutput=Function.sendMail(subject,msg ,None,recipients)
                        
        print(" schedule ends at "+strdatetime)
    
    
    def schedule():
        try:
            sched = BackgroundScheduler(daemon=True)
            sched.add_job(func=Function.updateDatabase,trigger='interval',minutes=20)
            sched.start()
        except Exception as e:
            if(sched.running):
                print('shutdown')
                sched.shutdown()

   