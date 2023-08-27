# Imports
from database import Database
from flask import jsonify, request

class CourseApplication:
    # Class init
    def __init__(self):
        self.db = Database()
        self.noData = "Nema podataka"

    # Course application
    def courseApplication(self, userid, courseid):
        db = self.db.connectDB()
        cursor = db.cursor()
        
        sql = "INSERT INTO courseapplication(userid, courseid) VALUES (?, ?)"
        cursor.execute(sql, [userid, courseid])
        db.commit()
        db.close()
        
        return True

    # Get last hour
    def getLastHour(self, courseid):
        db = self.db.connectDB()
        cursor = db.cursor()

        sql = "SELECT u.id, u.usertype, ut.typename, ca.courseid, c.coursename, u.name, u.email, MAX(DATETIME(ca.logindate)) FROM users u JOIN usertype ut ON u.usertype = ut.id JOIN courseapplication ca ON u.id = ca.userid JOIN courses c ON ca.courseid = c.id WHERE DATETIME(ca.logindate) >= DATETIME('NOW', '-1 Hour') AND u.usertype = 1 AND ca.courseid = ? GROUP BY u.id, u.usertype, ut.typename, ca.courseid, c.coursename, u.name, u.email ORDER BY logindate DESC"
        cursor.execute(sql, [courseid])
        data = cursor.fetchall()
        db.close()

        return data

    ################ ENDPOINTS Methods #####################
    # Course application
    def epCourseApplication(self):
        details = request.get_json()
        userid = details["userid"]
        courseid = details["courseid"]

        result = self.courseApplication(userid, courseid)
        if not result:
            return jsonify({"msg": self.noData})
 
        return jsonify(result)
    
    # Get last hour
    def epGetLastHour(self, courseid):
        data = self.getLastHour(courseid)

        items = []
        for item in data:
            items.append({"id": item[0], "usertype": item[1], "typename": item[2], "courseid": item[3], "coursename": item[4], "name": item[5], "email": item[6], "logindate": item[7]})
    
        return jsonify({"courseapplication": items})