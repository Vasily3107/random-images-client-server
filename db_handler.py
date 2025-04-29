from pyodbc import connect as connect_to_db
server   = 'localhost\SQLEXPRESS'
database = 'test_db'
dsn      =f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

from uuid import UUID, uuid4

class DBHandler:
    '''
    Admin panel database handler
    '''

    @staticmethod
    def log_in(login:str, password:str) -> UUID | None:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('SELECT uuid FROM Administrators WHERE [login] = ? AND [password] = ?',
                    (login, password))

        try   : res = cur.fetchone()[0]
        except: res = None

        cur.close()
        con.close()
        return res


    @staticmethod
    def get_users() -> tuple[tuple[UUID, str]]:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('SELECT uuid, [login] FROM Users')
        res = cur.fetchall()

        cur.close()
        con.close()
        return res


    @staticmethod
    def get_user_logs(user_uuid:UUID) -> tuple[tuple[str, str, str]]:
        '''
        return tuple((uuid, date, message, url), ...)
        '''
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('SELECT uuid, [date], [message], [url] FROM UserLogs WHERE user_uuid = ? ORDER BY [date] DESC', (user_uuid,))
        res = cur.fetchall()

        cur.close()
        con.close()
        return res


    @staticmethod
    def update_log(log_uuid:UUID, column:str, value:str) -> None:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute(('UPDATE UserLogs '
                    f'SET {column} = ? '
                     'WHERE uuid = ?'),
                    (value, log_uuid))
        con.commit()

        cur.close()
        con.close()


    @staticmethod
    def add_log(user_uuid:UUID, msg:str, url:str, date:str) -> None:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('INSERT INTO UserLogs VALUES (NEWID(), ?, ?, ?, ?)',
                    (user_uuid, msg, url, date))
        con.commit()

        cur.close()
        con.close()


    @staticmethod
    def del_log(log_uuid:UUID) -> None:
        con = connect_to_db(dsn)
        cur = con.cursor()

        cur.execute('DELETE FROM UserLogs WHERE uuid = ?', (log_uuid,))
        con.commit()

        cur.close()
        con.close()