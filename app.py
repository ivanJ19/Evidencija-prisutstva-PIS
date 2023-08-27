# Imports
import os
import sys
from flask import Flask, request, render_template
sys.path.append('classes')
from flaskwrapper import FlaskAppWrapper
from flask_cors import CORS
from database import Database
from usertype import UserType
from users import Users
from login import Login
from courses import Courses
from courseapplication import CourseApplication
from profesorscourses import ProfesorsCourses
from studentscourses import StudentsCourses
from databasedata import DatabaseData

# Define app
flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)
CORS(flask_app)

# Init classes
ut = UserType()
u = Users()
l = Login()
c = Courses()
ca = CourseApplication()
pc = ProfesorsCourses()
sc = StudentsCourses()

# Create endpoints

# Usertype
app.add_endpoint('/usertype/all', 'epGetAllUserType', ut.epGetAll, methods=['GET'])
app.add_endpoint('/usertype/<int:id>', 'epGetByIdUserType', ut.epGetById, methods=['GET'])
app.add_endpoint('/usertype/<string:typename>', 'epGetByTypeNameUserType', ut.epGetByTypeName, methods=['GET'])
app.add_endpoint('/usertype/create', 'epInsertUserType', ut.epInsert, methods=['PUT'])
app.add_endpoint('/usertype/update/<int:id>', 'epUpdateUserType', ut.epUpdate, methods=['PUT'])
app.add_endpoint('/usertype/delete/<int:id>', 'epDeleteUserType', ut.epDelete, methods=['DELETE'])

# Users
app.add_endpoint('/users/all', 'epGetAllUsers', u.epGetAll, methods=['GET'])
app.add_endpoint('/users/<int:id>', 'epGetByIdUsers', u.epGetById, methods=['GET'])
app.add_endpoint('/users/typeid/<int:usertype>', 'epGetByUserTypeID', u.epGetByUserTypeID, methods=['GET'])
app.add_endpoint('/users/type/<string:typename>', 'epGetByTypeNameUsers', u.epGetByTypeName, methods=['GET'])
app.add_endpoint('/users/name/<string:name>', 'epGetByNameUsers', u.epGetByName, methods=['GET'])
app.add_endpoint('/users/email/<string:email>', 'epGetByEmailUsers', u.epGetByEmail, methods=['GET'])
app.add_endpoint('/users/create', 'epInsertUsers', u.epInsert, methods=['PUT'])
app.add_endpoint('/users/update/<int:id>', 'epUpdateUsers', u.epUpdate, methods=['PUT'])
app.add_endpoint('/users/delete/<int:id>', 'epDeleteUsers', u.epDelete, methods=['DELETE'])

# Login
app.add_endpoint('/login', 'epcheckLogin', l.epcheckLogin, methods=['POST'])
app.add_endpoint('/login/all', 'epGetAllLogin', l.epGetAll, methods=['GET'])

# Courses
app.add_endpoint('/courses/all', 'epGetAllCourses', c.epGetAll, methods=['GET'])
app.add_endpoint('/courses/<int:id>', 'epGetByIdCourses', c.epGetById, methods=['GET'])
app.add_endpoint('/courses/<string:coursename>', 'epGetByCourseName', c.epGetByCourseName, methods=['GET'])
app.add_endpoint('/courses/create', 'epInsertCourses', c.epInsert, methods=['PUT'])
app.add_endpoint('/courses/update/<int:id>', 'epUpdateCourses', c.epUpdate, methods=['PUT'])
app.add_endpoint('/courses/delete/<int:id>', 'epDeleteCourses', c.epDelete, methods=['DELETE'])

# Course application
app.add_endpoint('/courseapplication/app', 'epCourseApplication', ca.epCourseApplication, methods=['PUT'])
app.add_endpoint('/courseapplication/hour/<int:courseid>', 'epGetLastHour', ca.epGetLastHour, methods=['GET'])

# Profesors courses
app.add_endpoint('/profesorscourses/all', 'epGetAllProfesorsCourses', pc.epGetAll, methods=['GET'])
app.add_endpoint('/profesorscourses/<int:id>', 'epGetByIdProfesorsCourses', pc.epGetById, methods=['GET'])
app.add_endpoint('/profesorscourses/profesor/<int:profesorid>', 'epGetByProfesorIdProfesorsCourses', pc.epGetByProfesorId, methods=['GET'])
app.add_endpoint('/profesorscourses/create', 'epInsertProfesorsCourses', pc.epInsert, methods=['PUT'])
app.add_endpoint('/profesorscourses/update/<int:id>', 'epUpdateProfesorsCourses', pc.epUpdate, methods=['PUT'])
app.add_endpoint('/profesorscourses/updatebyprofessor/<int:profesorid>', 'epUpdateByProfessorCourses', pc.epUpdateByProfessor, methods=['PUT'])
app.add_endpoint('/profesorscourses/delete/<int:id>', 'epDeleteProfesorsCourses', pc.epDelete, methods=['DELETE'])

# Students courses
app.add_endpoint('/studentscourses/all', 'epGetAllStudentsCourses', sc.epGetAll, methods=['GET'])
app.add_endpoint('/studentscourses/<int:id>', 'epGetByIdStudentsCourses', sc.epGetById, methods=['GET'])
app.add_endpoint('/studentscourses/student/<int:studentid>', 'epGetByProfesorIdStudentsCourses', sc.epGetByStudentId, methods=['GET'])
app.add_endpoint('/studentscourses/course/<int:studentid>/<int:courseid>', 'epGetByStudentCourseId', sc.epGetByStudentCourseId, methods=['GET'])
app.add_endpoint('/studentscourses/create', 'epInsertStudentsCourses', sc.epInsert, methods=['PUT'])
app.add_endpoint('/studentscourses/update/<int:id>', 'epUpdateStudentsCourses', sc.epUpdate, methods=['PUT'])
app.add_endpoint('/studentscourses/delete/<int:id>', 'epDeleteStudentsCourses', sc.epDelete, methods=['DELETE'])

# Start app
if __name__ == '__main__':
    # Create tables
    ct = Database()
    ct.createTables()
    print("Tables created")
 
    # Init import data clasess
    dbdata = DatabaseData()   

    # User type data
    if ut.getCount() == 0:
        dbdata.UserTypeData() 
        print("User type records inserted")
    else:
        print("Skipping insert user type data")

    # Users data
    if u.getCount() == 0:
        dbdata.UsersData() 
        print("Users records inserted")
    else:
        print("Skipping insert users data")

    # Courses data
    if c.getCount() == 0:
        dbdata.CoursesData() 
        print("Courses records inserted")
    else:
        print("Skipping insert courses data")

    # Profesors courses data
    if pc.getCount() == 0:
        dbdata.ProfesorsCoursesData() 
        print("Profesors courses records inserted")
    else:
        print("Skipping insert profesors courses data")
 
    # Server enviroment and app run
    server_port = os.environ.get('PORT_NUMBER', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')

