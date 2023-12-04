import mysql.connector

class QuarantineDAO:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "root"
        self.database = "quarantine"
        self.connection = None
        self.cursor = None

    def getCursor(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def closeAll(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def create(self, values):
        cursor = self.getCursor()
        sql = "insert into quar (lot, part, qty, datein, reason, badge, badgeout, dateout, status, signoutcomment) values (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid
    
    def getAll(self):
        try:
            cursor = self.getCursor()
            # Change the cursor to return dictionaries
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM quar"
            cursor.execute(sql)
            result = cursor.fetchall()
           
            return result  # Ensure we're returning the fetched data
            
        except mysql.connector.Error as e:
            print("Database error:", e)  # Print out the error if any
        finally:
            self.closeAll()

    def findByID(self, lot):
        cursor = self.getCursor()
        cursor = self.connection.cursor(dictionary=True)
        sql="select * from quar where lot = %s"
        values = (lot,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return result
        self.closeAll()

    def update(self, values):
        cursor = self.getCursor()
        sql = "update quar set part = %s, qty = %s, datein = %s, reason = %s, badge = %s where lot = %s"
        cursor.execute(sql, (values['part'], values['qty'], values['datein'], values['reason'], values['badge'], values['lot']))
        self.connection.commit()
        print("update done")
        self.closeAll()

    def update_signout(self, lot, badgeout, dateout, signoutcomment):
        cursor = self.getCursor()
        sql = "UPDATE quar SET badgeout = %s, dateout = %s, signoutcomment = %s, status = 0 WHERE lot = %s"
        values = (badgeout, dateout, signoutcomment, lot)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()



    def delete(self, lot):
        cursor = self.getCursor()
        sql = "delete from quar where lot = %s"
        values = (lot,)
        cursor.execute(sql, values)
        self.connection.commit()
        print("delete done")
        self.closeAll()

    def getLotsWithStatus(self, status):
        try:
            cursor = self.getCursor()
            # Change the cursor to return dictionaries
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM quar WHERE status = %s"
            cursor.execute(sql, (status,))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print("Database error:", e)
        finally:
            self.closeAll()

    def search_records(self, search_query):
        cursor = self.getCursor()
        cursor = self.connection.cursor(dictionary=True)
        # Modify the SQL query to search for records based on your database structure
        sql = "SELECT * FROM quar WHERE lot LIKE %s OR part LIKE %s"
        values = (f"%{search_query}%", f"%{search_query}%")
        cursor.execute(sql, values)
        search_results = cursor.fetchall()
        self.closeAll()
        return search_results

    def get_operator_data(self):
            try:
                cursor = self.getCursor()
                # Change the cursor to return dictionaries
                cursor = self.connection.cursor(dictionary=True)
                sql = "SELECT * FROM operator"
                cursor.execute(sql)
                result = cursor.fetchall()
                operator_data = {record['badge']: record['operatorname'] for record in result}
                return operator_data
            except mysql.connector.Error as e:
                print("Database error:", e)
            finally:
                self.closeAll()
