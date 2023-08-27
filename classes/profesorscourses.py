# Imports
from database import Database
from flask import jsonify, request

# User type class
class ProfesorsCourses:
    # Class init
    def __init__(self):
        self.db = Database()
        self.noData = "Nema podataka"

    # Get all
    def getAll(self):
        db = self.db.connectDB()
        cursor = db.cursor()

        sql = "SELECT pc.id, pc.profesorid, u.name, u.email, pc.courseid, c.coursename, c.description, c.link FROM profesorscourses pc JOIN users u ON pc.profesorid = u.id JOIN courses c ON pc.courseid = c.id ORDER BY c.id ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()

        return data

    # Get by ID
    def getById(self, id):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT pc.id, pc.profesorid, u.name, u.email, pc.courseid, c.coursename, c.description, c.link FROM profesorscourses pc JOIN users u ON pc.profesorid = u.id JOIN courses c ON pc.courseid = c.id WHERE pc.id = ?"
        cursor.execute(sql, [id])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get by profesor ID
    def getByProfesorId(self, profesorid):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT pc.id, pc.profesorid, u.name, u.email, pc.courseid, c.coursename, c.description, c.link FROM profesorscourses pc JOIN users u ON pc.profesorid = u.id JOIN courses c ON pc.courseid = c.id WHERE pc.profesorid = ?"
        cursor.execute(sql, [profesorid])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get count 
    def getCount(self):
        return len(self.getAll())

    # Insert
    def insert(self, profesorid, courseid):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "INSERT INTO profesorscourses(profesorid, courseid) VALUES (?, ?)"
        cursor.execute(sql, [profesorid, courseid])
        db.commit()
        db.close()
        
        return True
    
    # Update
    def update(self, id, profesorid, courseid):
        db = self.db.connectDB()
        cursor = db.cursor()
     
        item = self.getById(id)
        if item is None:
            db.close()
            return False
     
        sql = "UPDATE profesorscourses SET profesorid = ?, courseid = ? WHERE id = ?"
        cursor.execute(sql, [profesorid, courseid, id])
        db.commit()
        db.close()
        
        return True
    
    # Update by Professor
    def updateByProfessor(self, profesorid, courseid):
        db = self.db.connectDB()
        cursor = db.cursor()
     
        item = self.getByProfesorId(profesorid)
        if item is None:
            db.close()
            return False
     
        sql = "UPDATE profesorscourses SET courseid = ? WHERE profesorid = ?"
        cursor.execute(sql, [courseid, profesorid])
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
     
        sql = "DELETE FROM profesorscourses WHERE id = ?"
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
            items.append({"id": item[0], "profesorid": item[1], "name": item[2], "email": item[3], "courseid": item[4], "coursename": item[5], "description": item[6], "link": item[7]})
    
        return jsonify({"profesorscourses": items})

    # Get by ID
    def epGetById(self, id):
        data = self.getById(id)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "profesorid": data[1], "name": data[2], "email": data[3], "courseid": data[4], "coursename": data[5], "description": data[6], "link": data[7]})

    # Get by profesor ID
    def epGetByProfesorId(self, profesorid):
        data = self.getByProfesorId(profesorid)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "profesorid": data[1], "name": data[2], "email": data[3], "courseid": data[4], "coursename": data[5], "description": data[6], "link": data[7]})

    # Insert
    def epInsert(self):
        details = request.get_json()
        profesorid = details["profesorid"]
        courseid = details["courseid"]

        result = self.insert(profesorid, courseid)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Update
    def epUpdate(self, id):
        details = request.get_json()
        profesorid = details["profesorid"]
        courseid = details["courseid"]

        result = self.update(id, profesorid, courseid)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)
    
    # Update by Professor
    def epUpdateByProfessor(self, profesorid):
        details = request.get_json()
        courseid = details["courseid"]

        result = self.updateByProfessor(profesorid, courseid)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Delete
    def epDelete(self, id):
        result = self.delete(id)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)


