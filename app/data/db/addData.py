import pymysql;
from connection import connect;

def add_user(data = None):
    if data:
        sql = """
        INSERT INTO Users (ID, Username, Password, FirstName, MiddleName, LastName, Email, Mobile, Address, ProfileImg)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        connection = connect()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (
                    data['ID'], 
                    data['Username'], 
                    data['Password'], 
                    data['FirstName'],
                    data['MiddleName'], 
                    data['LastName'], 
                    data['Email'], 
                    data['Mobile'],
                    data['Address'], 
                    data['ProfileImg']
                ))

                connection.commit()
                print(f"Success! User {data['ID']} Was Added")
        except pymysql.Error as e: 
            print(f"DB Error: {e}")
            connection.rollback()
            print(f"Any Changes Made for User {data['ID']} have been Removed")
        except Exception as e: print(f"? Error: {e}")
        finally: connection.close()
    else:
        print("Data Error: Nothing was Provided")
        
def add_search(data = None):
    if data:
        sql = """
        INSERT INTO SavedSearches (UserID, SearchNum, SearchKeys)
        VALUES (%s, %s, %s)
        """
        connection = connect()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (data['UserID'], data['SearchNum'], data['SearchKeys']))
                connection.commit()
                print(f"Success! Search {data['SearchNum']} for User {data['UserID']} Was Added")
        except pymysql.Error as e: 
            print(f"DB Error: {e}")
            connection.rollback()
            print(f"Any Changes Made for User {data['UserID']} have been Removed")
        except Exception as e: print(f"? Error: {e}")
        finally: connection.close()
    else:
        print("Data Error: Nothing was Provided")