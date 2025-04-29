from pyodbc import connect as connect_to_db
server   = 'localhost\SQLEXPRESS'
database = 'test_db'
dsn      =f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

from uuid import UUID, uuid4

class DBHandler:
    '''
    Server database handler
    '''

    @staticmethod
    def log_in(login:str, password:str) -> UUID | None:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('SELECT uuid FROM Users WHERE [login] = ? AND [password] = ?',
                    (login, password))

        try   : res = cur.fetchone()[0]
        except: res = None

        cur.close()
        con.close()
        return res


    @staticmethod
    def sign_up(login:str, password:str) -> UUID | None:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('SELECT uuid FROM Users WHERE [login] = ?', (login,))

        res = None
        if not cur.fetchone():
            res = uuid4()
            cur.execute('INSERT INTO Users VALUES (?, ?, ?)', (res, login, password))
            con.commit()

        cur.close()
        con.close()
        return res


    @staticmethod
    def log_user_act(user_uuid:UUID, message:str, url:str='N/A') -> None:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('INSERT INTO UserLogs VALUES (NEWID(), ?, ?, ?, GETDATE())',
                    (user_uuid, message, url))
        con.commit()

        cur.close()
        con.close()