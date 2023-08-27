# Imports
from database import Database
from flask import jsonify, request

# User type class
class UserType:
    # Class init
    def __init__(self):
        self.db = Database()
        self.noData = "Nema podataka"

    # Get all
    def getAll(self):
        db = self.db.connectDB()
        cursor = db.cursor()

        sql = "SELECT id, typename FROM usertype ORDER BY id ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()

        return data

    # Get by ID
    def getById(self, id):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT id, typename FROM usertype WHERE id = ?"
        cursor.execute(sql, [id])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get by type name
    def getByTypeName(self, type):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT id, typename FROM usertype WHERE typename = ?"
        cursor.execute(sql, [type])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get count 
    def getCount(self):
        return len(self.getAll())

    # Insert
    def insert(self, typename):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "INSERT INTO usertype(typename) VALUES (?)"
        cursor.execute(sql, [typename])
        db.commit()
        db.close()
        
        return True
    
    # Update
    def update(self, id, typename):
        db = self.db.connectDB()
        cursor = db.cursor()
     
        item = self.getById(id)
        if item is None:
            db.close()
            return False
     
        sql = "UPDATE usertype SET typename = ? WHERE id = ?"
        cursor.execute(sql, [typename, id])
        db.commit()
        db.close()
        
        return True
        
    # Delete
    def delete(self, id):
        db = self.db.connectDB()
        cursor = db.cursor()
     
        item = self.getById(id)
        if item is None:
            db.close()
            return False
     
        sql = "DELETE FROM usertype WHERE id = ?"
        cursor.execute(sql, [id])
        db.commit()
        db.close()
        
        return True


    ################ ENDPOINTS Methods #####################
    # Get all
    def epGetAll(self):
        data = self.getAll()

        items = []
        for item in data:
            items.append({"id": item[0], "usertype": item[1]})
    
        return jsonify({"usertype": items})

    # Get by ID
    def epGetById(self, id):
        data = self.getById(id)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "userytpe": data[1]})

    # Get by typename
    def epGetByTypeName(self, typename):
        data = self.getByTypeName(typename)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "userytpe": data[1]})

    # Insert
    def epInsert(self):
        details = request.get_json()
        typename = details["typename"]

        result = self.insert(typename)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Update
    def epUpdate(self, id):
        details = request.get_json()
        typename = details["typename"]

        result = self.update(id, typename)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Delete
    def epDelete(self, id):
        result = self.delete(id)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)


