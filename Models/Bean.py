from flask_restful import fields,reqparse


class loginModel():
    logindict={'username':fields.String(None),'password':fields.String(None)}
    username= str(None)
    password =str(None)

class AdminModel:

    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    name= fields.String(None)
    email = fields.String(None)
    mobile = fields.String(None)
    password= fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)

class CustomerModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    name= fields.String(None)
    mobile = fields.String(None)
    email = fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)
    
class CryptoCurrencyModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    coingeckoCryptoId= fields.String(None)
    name= fields.String(None)
    symbol= fields.String(None)
    image= fields.String(None)
    website= fields.String(None)
    sourceCode= fields.String(None)
    marketCap= fields.Float(None)
    marketCapRank= fields.Integer(None)
    fullyDiluatedValuation= fields.Float(None)
    totalVolume= fields.Float(None)
    circulatingSupply= fields.Float(None)
    totalSupply= fields.Float(None)
    maxSupply= fields.Float(None)
    ath= fields.Float(None)
    athChangePercentage= fields.Float(None)
    athDate= fields.String(None)
    atl= fields.Float(None)
    atlChangePercentage= fields.Float(None)
    atlDate= fields.String(None)
    roi= fields.Float(None)
    lastUpdated= fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)

class WatchListModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    cryptocurrencyId= fields.Integer(None)
    customerId= fields.Integer(None)
    minThreshold = fields.Float(None)
    maxThreshold = fields.Float(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)

class CategoriesModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    coingeckoCategoryId= fields.String(None)
    name= fields.String(None)
    link = fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)


class PlatformsModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    coingeckoPlatformId= fields.String(None)
    name= fields.String(None)
    shortname= fields.String(None)
    chainIdentifier = fields.Integer(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)

class CryptocurrencyCategoryMappingModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    cryptocurrencyId= fields.Integer(None)
    categoryId= fields.Integer(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)
    categoryObj=CategoriesModel()
    cryptocurrencyObj=CryptoCurrencyModel()

class CryptocurrencyPlatformMappingModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    cryptocurrencyId= fields.Integer(None)
    platformId= fields.Integer(None)
    contractAddress= fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)
    platformObj=PlatformsModel()
    cryptocurrencyObj=CryptoCurrencyModel()

class ExplorerModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    cryptocurrencyId= fields.Integer(None)
    name= fields.String(None)
    link = fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)

class CryptocurrencyHistoryModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    cryptocurrencyId= fields.Integer(None)
    current_price= fields.Float(None)
    high_24h= fields.Float(None)
    low_24h= fields.Float(None)
    price_change_24h= fields.Float(None)
    market_cap_change_24h= fields.Float(None)
    market_cap_change_percentage_24h= fields.Float(None)
    price_change_percentage_1h_in_currency= fields.Float(None)
    price_change_percentage_24h_in_currency= fields.Float(None)
    price_change_percentage_7d_in_currency= fields.Float(None)
    price_change_percentage_14d_in_currency= fields.Float(None)
    price_change_percentage_30d_in_currency= fields.Float(None)
    price_change_percentage_200d_in_currency= fields.Float(None)
    price_change_percentage_1y_in_currency= fields.Float(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)

class CommunityModel:
    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    cryptocurrencyId= fields.Integer(None)
    name= fields.String(None)
    link = fields.String(None)
    image = fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(1)



class TokenObject:
    id=fields.Integer(None)
    loginAs=fields.String(None)
    def __init__(self,id,loginAs):
        self.id=id
        self.loginAs=loginAs

