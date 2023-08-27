# Imports
from database import Database
from flask import jsonify, request

# User type class
class Courses:
    # Class init
    def __init__(self):
        self.db = Database()
        self.noData = "Nema podataka"

    # Get all
    def getAll(self):
        db = self.db.connectDB()
        cursor = db.cursor()

        sql = "SELECT id, coursename, description, link FROM courses ORDER BY id ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()

        return data

    # Get by ID
    def getById(self, id):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT id, coursename, description, link FROM courses WHERE id = ?"
        cursor.execute(sql, [id])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get by type course name
    def getByCourseName(self, coursename):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SSELECT id, coursename, description, link FROM courses WHERE coursename = ?"
        cursor.execute(sql, [coursename])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get count 
    def getCount(self):
        return len(self.getAll())

    # Insert
    def insert(self, coursename, description, link):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "INSERT INTO courses(coursename, description, link) VALUES (?, ?, ?)"
        cursor.execute(sql, [coursename, description, link])
        db.commit()
        db.close()
        
        return True
    
    # Update
    def update(self, id, coursename, description, link):
        db = self.db.connectDB()
        cursor = db.cursor()
     
        item = self.getById(id)
        if item is None:
            db.close()
            return False
     
        sql = "UPDATE courses SET coursename = ?, description = ?, link = ? WHERE id = ?"
        cursor.execute(sql, [coursename, description, link, id])
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
     
        sql = "DELETE FROM courses WHERE id = ?"
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
            items.append({"id": item[0], "coursename": item[1], "description": item[2], "link": item[3]})
    
        return jsonify({"courses": items})

    # Get by ID
    def epGetById(self, id):
        data = self.getById(id)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "coursename": data[1], "description": data[2], "link": data[3]})

    # Get by coursename
    def epGetByCourseName(self, coursename):
        data = self.getByCourseName(coursename)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "coursename": data[1], "description": data[2], "link": data[3]})

    # Insert
    def epInsert(self):
        details = request.get_json()
        coursename = details["coursename"]
        description = details["description"]
        link = details["link"]

        result = self.insert(coursename, description, link)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Update
    def epUpdate(self, id):
        details = request.get_json()
        coursename = details["coursename"]
        description = details["description"]
        link = details["link"]

        result = self.update(id, coursename, description, link)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Delete
    def epDelete(self, id):
        result = self.delete(id)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)


