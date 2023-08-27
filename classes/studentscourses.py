# Imports
from database import Database
from flask import jsonify, request

# User type class
class StudentsCourses:
    # Class init
    def __init__(self):
        self.db = Database()
        self.noData = "Nema podataka"

    # Get all
    def getAll(self):
        db = self.db.connectDB()
        cursor = db.cursor()

        sql = "SELECT sc.id, sc.studentid, u.name, u.email, sc.courseid, c.coursename, c.description, c.link, sc.grade FROM studentscourses sc JOIN users u ON sc.studentid = u.id JOIN courses c ON sc.courseid = c.id ORDER BY sc.id ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()

        return data

    # Get by ID
    def getById(self, id):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT sc.id, sc.studentid, u.name, u.email, sc.courseid, c.coursename, c.description, c.link, sc.grade FROM studentscourses sc JOIN users u ON sc.studentid = u.id JOIN courses c ON sc.courseid = c.id WHERE sc.id = ?"
        cursor.execute(sql, [id])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get by student ID
    def getByStudentId(self, studentid):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT sc.id, sc.studentid, u.name, u.email, sc.courseid, c.coursename, c.description, c.link, sc.grade FROM studentscourses sc JOIN users u ON sc.studentid = u.id JOIN courses c ON sc.courseid = c.id WHERE sc.studentid = ?"
        cursor.execute(sql, [studentid])
        data = cursor.fetchall()
        db.close()
        
        return data

    # Get by student and course ID
    def getByStudentCourseId(self, studentid, courseid):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "SELECT sc.id, sc.studentid, u.name, u.email, sc.courseid, c.coursename, c.description, c.link, sc.grade FROM studentscourses sc JOIN users u ON sc.studentid = u.id JOIN courses c ON sc.courseid = c.id WHERE sc.studentid = ? AND sc.courseid = ?"
        cursor.execute(sql, [studentid, courseid])
        data = cursor.fetchone()
        db.close()
        
        return data

    # Get count 
    def getCount(self):
        return len(self.getAll())

    # Insert
    def insert(self, studentid, courseid, grade):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "INSERT INTO studentscourses(studentid, courseid, grade) VALUES (?, ?, ?)"
        cursor.execute(sql, [studentid, courseid, grade])
        db.commit()
        db.close()
        
        return True
    
    # Update
    def update(self, id, studentid, courseid, grade):
        db = self.db.connectDB()
        cursor = db.cursor()
     
        item = self.getById(id)
        if item is None:
            db.close()
            return False
     
        sql = "UPDATE studentscourses SET studentid = ?, courseid = ?, grade = ? WHERE id = ?"
        cursor.execute(sql, [studentid, courseid, grade, id])
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
     
        sql = "DELETE FROM studentscourses WHERE id = ?"
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
            items.append({"id": item[0], "studentid": item[1], "name": item[2], "email": item[3], "courseid": item[4], "coursename": item[5], "description": item[6], "link": item[7], "grade": item[8]})
    
        return jsonify({"studentscourses": items})

    # Get by ID
    def epGetById(self, id):
        data = self.getById(id)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "studentid": data[1], "name": data[2], "email": data[3], "courseid": data[4], "coursename": data[5], "description": data[6], "link": data[7], "grade": data[8]})

    # Get by student and course ID
    def epGetByStudentCourseId(self, studentid, courseid):
        data = self.getByStudentCourseId(studentid, courseid)

        if data is None:
            return jsonify({"msg": self.noData})
    
        return jsonify({"id": data[0], "studentid": data[1], "name": data[2], "email": data[3], "courseid": data[4], "coursename": data[5], "description": data[6], "link": data[7], "grade": data[8]})

    # Get by student ID
    def epGetByStudentId(self, studentid):
        data = self.getByStudentId(studentid)

        items = []
        for item in data:
            items.append({"id": item[0], "studentid": item[1], "name": item[2], "email": item[3], "courseid": item[4], "coursename": item[5], "description": item[6], "link": item[7], "grade": item[8]})
    
        return jsonify({"studentscourses": items})

    # Insert
    def epInsert(self):
        details = request.get_json()
        studentid = details["studentid"]
        courseid = details["courseid"]
        grade = details["grade"]

        result = self.insert(studentid, courseid, grade)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Update
    def epUpdate(self, id):
        details = request.get_json()
        studentid = details["studentid"]
        courseid = details["courseid"]
        grade = details["grade"]

        result = self.update(id, studentid, courseid, grade)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)

    # Delete
    def epDelete(self, id):
        result = self.delete(id)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)


