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
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM quar"
            cursor.execute(sql)
            result = cursor.fetchall()
           
            return result  
            
        except mysql.connector.Error as e:
            print("Database error:", e)  
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

    # updates the quar table based on the data provided by the operator when signing out the parts from quarantine
    def update_signout(self, lot, badgeout, dateout, signoutcomment):
        cursor = self.getCursor()
        sql = "UPDATE quar SET badgeout = %s, dateout = %s, signoutcomment = %s, status = 0 WHERE lot = %s"
        values = (badgeout, dateout, signoutcomment, lot)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()


    # carries out delete functionality
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
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM quar WHERE status = %s"
            cursor.execute(sql, (status,))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print("Database error:", e)
        finally:
            self.closeAll()

    # searches the quar table using the string entered in the search box on the search page
    def search_records(self, search_query):
        cursor = self.getCursor()
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM quar WHERE lot LIKE %s OR part LIKE %s"
        values = (f"%{search_query}%", f"%{search_query}%")
        cursor.execute(sql, values)
        search_results = cursor.fetchall()
        self.closeAll()
        return search_results

    # pulls the operator name from a separate table in the database by checking badge number, returns dictionary
    def get_operator_data(self):
            try:
                cursor = self.getCursor()
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

    def get_building_data(self, building_name=None):
        cursor = self.getCursor()
        cursor = self.connection.cursor(dictionary=True)
        query = """
        SELECT building, COUNT(lot) as lot_count, SUM(qty) as total_qty
        FROM quar
        """
        if building_name:
            query += f"WHERE building = '{building_name}'"
        query += " GROUP BY building"

        cursor.execute(query)
        result_set = cursor.fetchall()
        buildings_data = [
            {'name': row['building'], 'lot_count': row['lot_count'], 'total_qty': row['total_qty']}
            for row in result_set]

        return buildings_data
