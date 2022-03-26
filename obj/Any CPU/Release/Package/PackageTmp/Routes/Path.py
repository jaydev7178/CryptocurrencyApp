import sys
import inspect
from apispec import APISpec
from Controllers.AdminUser import *
from Controllers.Customers import *
from Controllers.Categories import *
from Controllers.Community import *
from Controllers.Cryptocurrencies import *
from Controllers.CryptocurrencyCategoryMapping import *
from Controllers.CryptocurrencyHistory import *
from Controllers.CryptocurrencyPlatformMapping import *
from Controllers.Explorers import *
from Controllers.Platforms import *
from Controllers.WatchList import *
from Models.Bean import *

def initalize_routes(api):
    #AdminUser
    #region 
    api.add_resource(SaveAdminUser, "/adminuser/saveAdminUser",methods=[ 'POST'])
    api.add_resource(GetAdminUserList, "/adminuser/getAdminUserList",methods=[ 'POST'])
    api.add_resource(DisableEnableAdminUser, "/adminuser/disableAdminUser",endpoint='disableAdminUser',methods=[ 'POST'])
    api.add_resource(DisableEnableAdminUser, "/adminuser/enableAdminUser",endpoint='enableAdminUser',methods=[ 'POST'])
    api.add_resource(DeleteAdminUser, "/adminuser/deleteAdminUser",methods=[ 'POST'])
    api.add_resource(LoginAdminUser, "/adminuser/login",methods=[ 'POST'])
    
    #endregion 

    #Customers
    #region 
    api.add_resource(SaveCustomer, "/customer/saveCustomer",methods=[ 'POST'])
    api.add_resource(GetCustomerList, "/customer/getCustomerList",methods=[ 'POST'])
    api.add_resource(DisableEnableCustomer, "/customer/disableCustomer",endpoint='disableCustomer',methods=[ 'POST'])
    api.add_resource(DisableEnableCustomer, "/customer/enableCustomer",endpoint='enableCustomer',methods=[ 'POST'])
    api.add_resource(DeleteCustomer, "/customer/deleteCustomer",methods=[ 'POST'])
    api.add_resource(LoginCustomer, "/customer/login",methods=[ 'POST'])
    
    #endregion 
    
    #Categories
    #region 
    api.add_resource(SaveCategory, "/category/saveCategory",methods=[ 'POST'])
    api.add_resource(GetCategoryList, "/category/getCategoryList",methods=[ 'POST'])
    api.add_resource(DisableEnableCategory, "/category/disableCategory",endpoint='disableCategory',methods=[ 'POST'])
    api.add_resource(DisableEnableCategory, "/category/enableCategory",endpoint='enableCategory',methods=[ 'POST'])
    api.add_resource(DeleteCategory, "/category/deleteCategory",methods=[ 'POST'])
    api.add_resource(PermanentDeleteCategory, "/category/permanentDeleteCategory",methods=[ 'POST'])
    api.add_resource(UpdateCategories, "/category/updateCategories",methods=[ 'POST'])
    
    #endregion 
    
    #Community
    #region 
    api.add_resource(SaveCommunity, "/community/saveCommunity",methods=[ 'POST'])
    api.add_resource(GetCommunityList, "/community/getCommunityList",methods=[ 'POST'])
    api.add_resource(DisableEnableCommunity, "/community/disableCommunity",endpoint='disableCommunity',methods=[ 'POST'])
    api.add_resource(DisableEnableCommunity, "/community/enableCommunity",endpoint='enableCommunity',methods=[ 'POST'])
    api.add_resource(DeleteCommunity, "/community/deleteCommunity",methods=[ 'POST'])
    
    #endregion 

    
    #Cryptocurrencies
    #region 
    api.add_resource(SaveCryptocurrency, "/cryptocurrency/saveCryptocurrency",methods=[ 'POST'])
    api.add_resource(UpdateCryptocurrencyData, "/cryptocurrency/updateCryptocurrencyData",methods=[ 'POST'])
    api.add_resource(UpdateCryptocurrencyDetails, "/cryptocurrency/updateCryptocurrencyDetails",methods=[ 'POST'])
    api.add_resource(GetCryptocurrencyList, "/cryptocurrency/getCryptocurrencyList",methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrency, "/cryptocurrency/disableCryptocurrency",endpoint='disableCryptocurrency',methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrency, "/cryptocurrency/enableCryptocurrency",endpoint='enableCryptocurrency',methods=[ 'POST'])
    api.add_resource(DeleteCryptocurrency, "/cryptocurrency/deleteCryptocurrency",methods=[ 'POST'])
    api.add_resource(PermanentDeleteCryptocurrency, "/cryptocurrency/permanentDeleteCryptocurrency",methods=[ 'POST'])
    
    #endregion 
    
    #CryptocurrencyCategoryMapping
    #region 
    api.add_resource(SaveCryptocurrencyCategoryMapping, "/cryptocurrencycategory/saveCryptocurrencyCategory",methods=[ 'POST'])
    api.add_resource(GetCryptocurrencyCategoryMappingList, "/cryptocurrencycategory/getCryptocurrencyCategoryList",methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrencyCategoryMapping, "/cryptocurrencycategory/disableCryptocurrencyCategory",endpoint='disableCryptocurrencyCategory',methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrencyCategoryMapping, "/cryptocurrencycategory/enableCryptocurrencyCategory",endpoint='enableCryptocurrencyCategory',methods=[ 'POST'])
    api.add_resource(DeleteCryptocurrencyCategoryMapping, "/cryptocurrencycategory/deleteCryptocurrencyCategory",methods=[ 'POST'])
    
    #endregion 
    
    #CryptocurrencyPlatformMapping
    #region 
    api.add_resource(SaveCryptocurrencyPlatformMapping, "/cryptocurrencyplatform/saveCryptocurrencyPlatform",methods=[ 'POST'])
    api.add_resource(GetCryptocurrencyPlatformMappingList, "/cryptocurrencyplatform/getCryptocurrencyPlatformMappingList",methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrencyPlatformMapping, "/cryptocurrencyplatform/disableCryptocurrencyPlatform",endpoint='disableCryptocurrencyPlatform',methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrencyPlatformMapping, "/cryptocurrencyplatform/enableCryptocurrencyPlatform",endpoint='enableCryptocurrencyPlatform',methods=[ 'POST'])
    api.add_resource(DeleteCryptocurrencyPlatformMapping, "/cryptocurrencyplatform/deleteCryptocurrencyPlatform",methods=[ 'POST'])
    
    #endregion 
    
    #CryptocurrencyHistory
    #region 
    api.add_resource(SaveCryptocurrencyHistory, "/cryptocurrencyhistory/saveCryptocurrencyHistory",methods=[ 'POST'])
    api.add_resource(GetCryptocurrencyHistoryList, "/cryptocurrencyhistory/getCryptocurrencyHistoryList",methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrencyHistory, "/cryptocurrencyhistory/disableCryptocurrencyHistory",endpoint='disableCryptocurrencyHistory',methods=[ 'POST'])
    api.add_resource(DisableEnableCryptocurrencyHistory, "/cryptocurrencyhistory/enableCryptocurrencyHistory",endpoint='enableCryptocurrencyHistory',methods=[ 'POST'])
    api.add_resource(DeleteCryptocurrencyHistory, "/cryptocurrencyhistory/deleteCryptocurrencyHistory",methods=[ 'POST'])
    
    #endregion 

    
    #Explorers
    #region 
    api.add_resource(SaveExplorer, "/explorer/saveExplorer",methods=[ 'POST'])
    api.add_resource(GetExplorerList, "/explorer/getExplorerList",methods=[ 'POST'])
    api.add_resource(DisableEnableExplorer, "/explorer/disableExplorer",endpoint='disableExplorer',methods=[ 'POST'])
    api.add_resource(DisableEnableExplorer, "/explorer/enableExplorer",endpoint='enableExplorer',methods=[ 'POST'])
    api.add_resource(DeleteExplorer, "/explorer/deleteExplorer",methods=[ 'POST'])
    
    #endregion 

    
    #Platforms
    #region 
    api.add_resource(SavePlatform, "/platform/savePlatform",methods=[ 'POST'])
    api.add_resource(GetPlatformList, "/platform/getPlatformList",methods=[ 'POST'])
    api.add_resource(DisableEnablePlatform, "/platform/disablePlatform",endpoint='disablePlatform',methods=[ 'POST'])
    api.add_resource(DisableEnablePlatform, "/platform/enablePlatform",endpoint='enablePlatform',methods=[ 'POST'])
    api.add_resource(DeletePlatform, "/platform/deletePlatform",methods=[ 'POST'])
    api.add_resource(PermanentDeletePlatform, "/platform/permanentDeletePlatform",methods=[ 'POST'])
    
    #endregion 
    
    #WatchList
    #region 
    api.add_resource(SaveWatchList, "/watchlist/saveWatchList",methods=[ 'POST'])
    api.add_resource(GetWatchList, "/watchlist/getWatchListList",methods=[ 'POST'])
    api.add_resource(DisableEnableWatchList, "/watchlist/disableWatchList",endpoint='disableWatchList',methods=[ 'POST'])
    api.add_resource(DisableEnableWatchList, "/watchlist/enableWatchList",endpoint='enableWatchList',methods=[ 'POST'])
    api.add_resource(DeleteWatchList, "/watchlist/deleteWatchList",methods=[ 'POST'])
    
    #endregion 



    return api


def initalize_swagger(docs):

    #AdminUser
    #region 
    docs.register(SaveAdminUser)
    docs.register(GetAdminUserList)
    docs.register(DisableEnableAdminUser,endpoint='disableAdminUser')
    docs.register(DisableEnableAdminUser,endpoint='enableAdminUser')
    docs.register(DeleteAdminUser)
    docs.register(LoginAdminUser)
    #endregion 
    
    #Customers
    #region 
    docs.register(SaveCustomer)
    docs.register(GetCustomerList)
    docs.register(DisableEnableCustomer,endpoint='disableCustomer')
    docs.register(DisableEnableCustomer,endpoint='enableCustomer')
    docs.register(DeleteCustomer)
    docs.register(LoginCustomer)
    #endregion 

    #Categories
    #region 
    docs.register(SaveCategory)
    docs.register(GetCategoryList)
    docs.register(DisableEnableCategory,endpoint='disableCategory')
    docs.register(DisableEnableCategory,endpoint='enableCategory')
    docs.register(DeleteCategory)
    docs.register(PermanentDeleteCategory)
    docs.register(UpdateCategories)
    #endregion 
    
    #Community
    #region 
    docs.register(SaveCommunity)
    docs.register(GetCommunityList)
    docs.register(DisableEnableCommunity,endpoint='disableCommunity')
    docs.register(DisableEnableCommunity,endpoint='enableCommunity')
    docs.register(DeleteCommunity)
    #endregion 
    
    #Cryptocurrency
    #region 
    docs.register(SaveCryptocurrency)
    docs.register(UpdateCryptocurrencyData)
    docs.register(UpdateCryptocurrencyDetails)
    docs.register(GetCryptocurrencyList)
    docs.register(DisableEnableCryptocurrency,endpoint='disableCryptocurrency')
    docs.register(DisableEnableCryptocurrency,endpoint='enableCryptocurrency')
    docs.register(DeleteCryptocurrency)
    docs.register(PermanentDeleteCryptocurrency)
    #endregion 

    
    #CryptocurrencyCategoryMapping
    #region 
    docs.register(SaveCryptocurrencyPlatformMapping)
    docs.register(GetCryptocurrencyPlatformMappingList)
    docs.register(DisableEnableCryptocurrencyPlatformMapping,endpoint='disableCryptocurrencyPlatform')
    docs.register(DisableEnableCryptocurrencyPlatformMapping,endpoint='enableCryptocurrencyPlatform')
    docs.register(DeleteCryptocurrencyPlatformMapping)
    #endregion 
    
    #CryptocurrencyCategoryMapping
    #region 
    docs.register(SaveCryptocurrencyCategoryMapping)
    docs.register(GetCryptocurrencyCategoryMappingList)
    docs.register(DisableEnableCryptocurrencyCategoryMapping,endpoint='disableCryptocurrencyCategory')
    docs.register(DisableEnableCryptocurrencyCategoryMapping,endpoint='enableCryptocurrencyCategory')
    docs.register(DeleteCryptocurrencyCategoryMapping)
    #endregion 
    
    #CryptocurrencyHistory
    #region 
    docs.register(SaveCryptocurrencyHistory)
    docs.register(GetCryptocurrencyHistoryList)
    docs.register(DisableEnableCryptocurrencyHistory,endpoint='disableCryptocurrencyHistory')
    docs.register(DisableEnableCryptocurrencyHistory,endpoint='enableCryptocurrencyHistory')
    docs.register(DeleteCryptocurrencyHistory)
    #endregion 
    
    #Explorers
    #region 
    docs.register(SaveExplorer)
    docs.register(GetExplorerList)
    docs.register(DisableEnableExplorer,endpoint='disableExplorer')
    docs.register(DisableEnableExplorer,endpoint='enableExplorer')
    docs.register(DeleteExplorer)
    #endregion 
    
    #Platforms
    #region 
    docs.register(SavePlatform)
    docs.register(GetPlatformList)
    docs.register(DisableEnablePlatform,endpoint='disablePlatform')
    docs.register(DisableEnablePlatform,endpoint='enablePlatform')
    docs.register(DeletePlatform)
    #endregion 
    
    #WatchList
    #region 
    docs.register(SaveWatchList)
    docs.register(GetWatchList)
    docs.register(DisableEnableWatchList,endpoint='disableWatchList')
    docs.register(DisableEnableWatchList,endpoint='enableWatchList')
    docs.register(DeleteWatchList)
    #endregion 






    return docs