from .Function import Function
from .Constant import Constant
from flask_restful import request

class JWTRequestFilter:
    @staticmethod
    def checkToken():
        reqpath=request.path
        if(reqpath!=None):
            token=JWTRequestFilter.checkJWTToken()
            if(token):
                tokenObj=Function.validateToken(token)
                if(tokenObj=="201" or tokenObj=="INVALID:LOGIN"):
                    return "INVALID:LOGIN"
                return tokenObj;
            else:
                return "INVALID:NOTOKEN"
        else:
            return "INVALID:LOGIN"


    #    @staticmethod
    #def checkToken():
    #    reqpath=request.path
    #    if(reqpath!=None):
    #        if(JWTRequestFilter.isJWTRequired(reqpath)):
    #            token=JWTRequestFilter.checkJWTToken()
    #            if(token):
    #                tokenObj=Function.validateToken(token)
    #                if(tokenObj=="201" or tokenObj=="INVALID:LOGIN"):
    #                    return "INVALID:LOGIN"
    #                return tokenObj;
    #            else:
    #                return "INVALID:NOTOKEN"
    #        else:
    #            return None
    #    else:
    #        return "INVALID:LOGIN"

    @staticmethod
    def isJWTRequired(reqpath):
        if reqpath in Constant.NoneTokenURL.values():
            return False
        else:
            return True
    @staticmethod
    def checkJWTToken():
        token=request.headers.get("token")
        if(token==None):
            return False
        return token