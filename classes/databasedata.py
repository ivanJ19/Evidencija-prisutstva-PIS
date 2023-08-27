# Imports
from usertype import UserType
from users import Users
from courses import Courses
from profesorscourses import ProfesorsCourses
from studentscourses import StudentsCourses

class DatabaseData:
    # Import user type data
    def UserTypeData(self):
        ut = UserType()
        ut.insert("Student")
        ut.insert("Profesor")

    # Import users data
    def UsersData(self):
        u = Users()
        u.insert(2, "Profesor 1", "profesor1@gmail.com", "7fa242fc775fc88106462384f4456131") # Password "ma635xd"

    # Import user type data
    def CoursesData(self):
        c = Courses()
        c.insert("Predmet 1", "Opis predmeta 1", "course.html")

    # Import profesors courses data
    def ProfesorsCoursesData(self):
        pc = ProfesorsCourses()
        pc.insert(1, 1);