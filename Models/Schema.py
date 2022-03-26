from marshmallow import Schema, fields


class TokenSchema(Schema):
    Token= fields.String(required=True,description="Please enter Token of user.")

class loginSchema(Schema):
    username= fields.String(description="Please enter username")
    password =fields.String(description="Please enter Password")

class SaveAdminUserSchema(Schema):
    id= fields.Integer(description="Please enter id")
    name =fields.String(description="Please enter Name")
    mobile =fields.String(description="Please enter Mobile")
    email =fields.String(description="Please enter Email")
    password =fields.String(description="Please enter Password",)

class SaveCustomersSchema(Schema):
    id= fields.Integer(description="Please enter id")
    name =fields.String(description="Please enter Name")
    mobile =fields.String(description="Please enter Mobile")
    email =fields.String(description="Please enter Email")
    password =fields.String(description="Please enter Password",)


class SaveCategorySchema(Schema):
    id= fields.Integer(description="Please enter id")
    coingeckoCategoryId =fields.Integer(description="Please enter coingecko category Id")
    name =fields.String(description="Please enter Name")
    link =fields.String(description="Please enter link")

class SaveCommunitySchema(Schema):
    id= fields.Integer(description="Please enter id")
    cryptocurrencyId =fields.Integer(description="Please enter cryptocurrency Id")
    name =fields.String(description="Please enter Name")
    link =fields.String(description="Please enter link")

class SaveWatchListSchema(Schema):
    id= fields.Integer(description="Please enter id")
    customerId= fields.Integer(description="Please enter customer Id")
    cryptocurrencyId =fields.Integer(description="Please enter cryptocurrency Id")
    minThreshold =fields.Float(description="Please enter minThreshold")
    maxThreshold =fields.Float(description="Please enter maxThreshold")

class SaveExplorerSchema(Schema):
    id= fields.Integer(description="Please enter id")
    cryptocurrencyId =fields.Integer(description="Please enter cryptocurrency Id")
    name =fields.String(required=True,description="Please enter Name")
    shortname =fields.String(description="Please enter shortname")
    chainIdentifier =fields.Integer(description="Please enter chainIdentifier")

class SavePlatformSchema(Schema):
    id= fields.Integer(description="Please enter id")
    coingeckoPlatformId =fields.String(description="Please enter coingeckoPlatform   Id")
    name =fields.String(description="Please enter Name")
    link =fields.String(description="Please enter link")

class SaveCryptocurrencySchema(Schema):
    coingeckoCryptoId =fields.String(description="Please enter coingecko crypto Id.")
    name =fields.String(description="Please enter Name.")
    symbol =fields.String(description="Please enter symbol.")
    image =fields.String(description="Please enter image.")
    website =fields.String(description="Please enter website.")
    sourceCode =fields.String(description="Please enter sourceCode.")
    marketCap =fields.Float(description="Please enter market Capital.")
    marketCapRank =fields.Int(description="Please enter market Capital Rank.")
    fullyDilutedValuation =fields.Float(description="Please enter fullyDilutedValuation.")
    totalVolume =fields.Float(description="Please enter totalVolume.")
    circulatingSupply =fields.Float(description="Please enter circulatingSupply.")
    totalSuppy =fields.Float(description="Please enter total Suppy.")
    maxSupply =fields.Float(description="Please enter max Supply.")
    ath =fields.Float(description="Please enter ath.")
    athChangePercentage =fields.Float(description="Please enter all time high price ChangePercentage.")
    athDate =fields.Str(description="Please enter all time highest price Date.")
    atl =fields.Float(description="Please enter all time lowest price.")
    atlChangePercentage =fields.Float(description="Please enter all time lowest price ChangePercentage.")
    atlDate =fields.Str(description="Please enter all time lowest price Date.")
    roi =fields.Float(description="Please enter return on investment.")

class SaveCryptocurrencyCategoryMappingSchema(Schema):
    id= fields.Integer(description="Please enter id.")
    categoryId= fields.Integer(description="Please enter category id.")
    cryptocurrencyId= fields.Integer(description="Please enter cryptocurrency Id.")

class SaveCryptocurrencyPlatformMappingSchema(Schema):
    id= fields.Integer(description="Please enter id.")
    platformId= fields.Integer(description="Please enter platform id.")
    cryptocurrencyId= fields.Integer(description="Please enter cryptocurrency Id.")

class SaveCryptocurrencyHistorySchema(Schema):
    id= fields.Integer(description="Please enter id.")
    cryptocurrencyId= fields.Integer(description="Please enter cryptocurrency Id.")
    currentPrice =fields.Float(description="Please enter currentPrice.")
    high24h =fields.Float(description="Please enter high24h.")
    low24h =fields.Float(description="Please enter low24h.")
    priceChange24h =fields.Float(description="Please enter priceChange24h.")
    marketCapChange24h =fields.Float(description="Please enter marketCapChange24h.")
    marketCapChangePercentage24h =fields.Float(description="Please enter marketCapChangePercentage24h.")
    priceChangePercentage1hInCurrency =fields.Float(description="Please enter priceChangePercentage1hInCurrency.")
    priceChangePercentage24hInCurrency =fields.Float(description="Please enter priceChangePercentage24hInCurrency.")
    priceChangePercentage7dInCurrency =fields.Float(description="Please enter priceChangePercentage7dInCurrency.")
    priceChangePercentage14dInCurrency =fields.Float(description="Please enter priceChangePercentage14dInCurrency.")
    priceChangePercentage30dInCurrency =fields.Float(description="Please enter priceChangePercentage30dInCurrency.")
    priceChangePercentage200dInCurrency =fields.Float(description="Please enter priceChangePercentage200dInCurrency.")
    priceChangePercentage1yInCurrency =fields.Float(description="Please enter priceChangePercentage1yInCurrency.")

class IdSchema(Schema):
    id= fields.Integer(description="Please enter id.")

class getWatchListSchema(Schema):
    id= fields.Integer(description="Please enter id.")
    cryptocurrencyId= fields.Integer(description="Please enter Cryptocurrency id.")
    customerId= fields.Integer(description="Please enter customer id.")

class getCoummunitySchema(Schema):
    id= fields.Integer(description="Please enter id.")
    cryptocurrencyId= fields.Integer(description="Please enter Cryptocurrency id.")

class getCryptocurrencyHistorySchema(Schema):
    id= fields.Integer(description="Please enter id.")
    cryptocurrencyId= fields.Integer(description="Please enter Cryptocurrency id.")

class getExplorerSchema(Schema):
    id= fields.Integer(description="Please enter id.")
    cryptocurrencyId= fields.Integer(description="Please enter Cryptocurrency id.")

class getCryptocurrencyPlatformMappingSchema(Schema):
    id= fields.Integer(description="Please enter id.")
    cryptocurrencyId= fields.Integer(description="Please enter Cryptocurrency id.")
    platformId= fields.Integer(description="Please enter platform id.")

class argsSchema(Schema):
    args= fields.String(default=None)

