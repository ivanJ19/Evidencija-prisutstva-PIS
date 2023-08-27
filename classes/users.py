# Imports
from database import Database
from flask import jsonify, request
import hashlib

# User type class
class Users:
    # Class init
    def __init__(self):
        self.db = Database()
        self.noData = "Nema podataka"

    # Get all
    def getAll(self):
        db = self.db.connectDB()
        cursor = db.cursor()

        sql = "SELECT u.id, u.usertype, ut.typename, u.name, u.email FROM users u JOIN usertype ut ON u.usertype = ut.id ORDER BY u.id ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()

        return data

    # Get by ID
    def getById(self, id):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT u.id, u.usertype, ut.typename, u.name, u.email FROM users u JOIN usertype ut ON u.usertype = ut.id WHERE u.id = ?"
        cursor.execute(sql, [id])
        data = cursor.fetchone()
        db.close()
        
        return data
    
    # Get by user type ID
    def getByUserTypeID(self, usertype):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT u.id, u.usertype, ut.typename, u.name, u.email FROM users u JOIN usertype ut ON u.usertype = ut.id WHERE u.usertype = ?"
        cursor.execute(sql, [usertype])
        data = cursor.fetchall()
        db.close()
        
        return data

    # Get by typename
    def getByTypeName(self, typename):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT u.id, u.usertype, ut.typename, u.name, u.email FROM users u JOIN usertype ut ON u.usertype = ut.id WHERE ut.typename = ?"
        cursor.execute(sql, [typename])
        data = cursor.fetchall()
        db.close()
        
        return data

    # Get by name
    def getByName(self, name):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT u.id, u.usertype, ut.typename, u.name, u.email FROM users u JOIN usertype ut ON u.usertype = ut.id WHERE u.name = ?"
        cursor.execute(sql, [name])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get by email
    def getByEmail(self, email):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT u.id, u.usertype, ut.typename, u.name, u.email FROM users u JOIN usertype ut ON u.usertype = ut.id WHERE u.email = ?"
        cursor.execute(sql, [email])
        data = cursor.fetchone()
        db.close()
        
        return data
    
    # Get max ID
    def getByMaxID(self):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT MAX(u.id) FROM users u"
        cursor.execute(sql)
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get count 
    def getCount(self):
        return len(self.getAll())

    # Insert
    def insert(self, usertype, name, email, password):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "INSERT INTO users(usertype, name, email, password) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, [usertype, name, email, password])
        db.commit()
        db.close()
        
        return True
    
    # Update
    def update(self, id, usertype, name, email, password):
        db = self.db.connectDB()
        cursor = db.cursor()
     
        item = self.getById(id)
        if item is None:
            db.close()
            return False
        
        if password != "":
            sql = "UPDATE users SET usertype = ?, name = ?, email = ?, password = ? WHERE id = ?"            
            cursor.execute(sql, [usertype, name, email, password, id])
        else:
            sql = "UPDATE users SET usertype = ?, name = ?, email = ? WHERE id = ?"
            cursor.execute(sql, [usertype, name, email, id])
        
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
     
        sql = "DELETE FROM users WHERE id = ?"
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
            items.append({"id": item[0], "usertype": item[1], "typename": item[2], "name": item[3], "email": item[4]})
    
        return jsonify({"users": items})

    # Get by ID
    def epGetById(self, id):
        data = self.getById(id)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "usertype": data[1], "typename": data[2], "name": data[3], "email": data[4]})
    
    # Get by user type ID
    def epGetByUserTypeID(self, usertype):
        data = self.getByUserTypeID(usertype)

        items = []
        for item in data:
            items.append({"id": item[0], "usertype": item[1], "typename": item[2], "name": item[3], "email": item[4]})
    
        return jsonify({"users": items})

    # Get by typename
    def epGetByTypeName(self, typename):
        data = self.getByTypeName(typename)

        items = []
        for item in data:
            items.append({"id": item[0], "usertype": item[1], "typename": item[2], "name": item[3], "email": item[4]})
    
        return jsonify({"users": items})

    # Get by name
    def epGetByName(self, name):
        data = self.getByName(name)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "usertype": data[1], "typename": data[2], "name": data[3], "email": data[4]})

    # Get by email
    def epGetByEmail(self, email):
        data = self.getByEmail(email)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "usertype": data[1], "typename": data[2], "name": data[3], "email": data[4]})

    # Insert
    def epInsert(self):
        details = request.get_json()
        usertype = details["usertype"]
        name = details["name"]
        email = details["email"]
        password = details["password"];

        Password = hashlib.md5()
        Password.update(password.encode("utf-8"))
        password = Password.hexdigest()

        result = self.insert(usertype, name, email, password)
        if not result:
            return jsonify({"msg": self.noData})
        
        data = self.getByMaxID()
 
        return jsonify({"id": data[0]})

    # Update
    def epUpdate(self, id):
        details = request.get_json()
        usertype = details["usertype"]
        name = details["name"]
        email = details["email"]
        password = details["password"];
        
        if password != "":
            Password = hashlib.md5()            
            Password.update(password.encode("utf-8"))
            password = Password.hexdigest()        

        result = self.update(id, usertype, name, email, password)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Delete
    def epDelete(self, id):
        result = self.delete(id)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)


