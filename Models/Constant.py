
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
    DatabaseConnectionString="DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\ProjectsV13;DATABASE="+DatabaseName
    #DatabaseConnectionString="Driver={SQL Server Native Client 11.0};Data Source=(localdb)\ProjectsV13;Database="+DatabaseName+";Initial Catalog=master;Integrated Security=True;Connect Timeout=30;Encrypt=False;TrustServerCertificate=False;ApplicationIntent=ReadWrite;MultiSubnetFailover=False;"
