
class Constant:    
    NoneTokenURL={
    "ADMIN_LOGIN_URL":"/api/v1/adminuser/login",
    "CUSTOMER_LOGIN_URL":"/api/v1/customers/login",
    "CUSTOMER_SAVE_URL":"/api/v1/customers/save"
    }

    ADMINUSER="adminuser"
    CUSTOMER="customer"
class DatabaseConstant:    
    DatabaseName="cryptocurrency_DB"
    DatabaseConnectionString="Driver={SQL Server Native Client 11.0};Server=(localdb)\MSSQLLocalDB;Database="+DatabaseName+";Trusted_Connection=yes;"
