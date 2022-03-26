import pypyodbc   
from Models.Constant import *
class Database:
    

    @staticmethod
    def insertData(sql):
        connection=None
        try:

            connection = pypyodbc.connect(DatabaseConstant.DatabaseConnectionString)
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.commit()
            connection.close()
        except BaseException as e:
            return e
        finally:
            if(connection!=None):
                if(connection.connect==1):
                    connection.close()
        return "200"

    @staticmethod
    def getCursor(sql):
        connection=None
        data=None
        try:
            connection = pypyodbc.connect(DatabaseConstant.DatabaseConnectionString)
            cursor = connection.cursor()
            cursor.execute(sql)
            data=cursor.fetchall()            
            connection.close()
        except Exception as e:
            return "201"
        finally:
            if(connection!=None):
                if(connection.connect==1):
                    connection.close()

        return data

    @staticmethod
    def getValue(sql):
        connection=None
        try:
            connection = pypyodbc.connect(DatabaseConstant.DatabaseConnectionString)
            cursor = connection.cursor()
            cursor.execute(sql)
            
            data=cursor.fetchone();
            if(data):
                data=data[0];
            connection.close()
        except Exception as e:
            return "201"
        finally:
            if(connection!=None):
                if(connection.connect==1):
                    connection.close()
        return data

    
        

