import smtplib
from email.mime.text import MIMEText


def readStudents(filePath):
    students_list = []
    with open(filePath) as file_object:
        for line in file_object.read().splitlines():
            if len(line.rsplit(",")) < 4:
                continue

            email = line.rsplit(",")[0]
            name = line.rsplit(",")[1]
            surname = line.rsplit(",")[2]
            points = int(line.rsplit(",")[3])
            grade = ""

            if len(line.rsplit(",")) > 5:
                grade = float(line.rsplit(",")[4])
                status = line.rsplit(",")[5]
            else:
                status = ""
            student = {"email": email, "name": name, "surname": surname, "points": points, "grade" : grade, "status": status}
            students_list.append(student)

    return students_list

def setGrade(points):
    points = int(points)
    if points <= 50:
        return 2
    elif 51 <= points <= 60:
        return 3
    elif 61 <= points <= 70:
        return 3.5
    elif 71 <= points <= 80:
        return 4
    elif 81 <= points <= 90:
        return 4.5
    elif points >= 91:
        return 5

def setGradesForStudents(students):
    for student in students:
        if (student["status"] == ""):
            student["grade"] = setGrade(student["points"])
            student["status"] = "graded"

def showStudents(students):
    for student in students:
        print(student, '\n')

def addStudent(studentsList, *studentArgs):
    if(len(studentArgs) < 4):
        print("za malo argumentow")
        return
    email = studentArgs[0]
    name = studentArgs[1]
    surname = studentArgs[2]
    points = int(studentArgs[3])
    grade = ""
    status = ""

    for student in studentsList:
        if student["email"] == email:
            print("student o podanym mailu juz istnieje")
            return

    if (len(studentArgs) > 4):
        grade = studentArgs[4]
        status = studentArgs[5]
    newStudent = {"email": email, "name": name, "surname": surname, "points": points, "grade": grade, "status": status}
    students.append(newStudent)
    print("pomyslnie dodano studenta")

def deleteStudent (studentsList, email):
    for i in range(len(studentsList)):
        if studentsList[i]["email"] == email:
            del studentsList[i]
            print("student deleted")
            return

    print("Nie znaleziono studenta o podanym adresie email")

def sendEmail(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()
def sendEmailToStudents(studentList):

    password = "aqoegpdmacnbplfd"
    sender = "ppy.pjatk@gmail.com"
    for student in studentList:
        if(student['status'] == "graded"):
            recipient = [student['email']]
            body = "Twoja ocena to: " + str(student['grade'])
            sendEmail("Wystawienie oceny", body, sender, recipient, password)
            student['status'] = "mailed"

def saveChangesToFile(students, filePath):

    with open(filePath, "w") as file_object:
        for student in students:
            line = f"{student['email']},{student['name']},{student['surname']},{student['points']}"
            if student['grade'] != '':
                line += f",{student['grade']},{student['status']}\n"
            else:
                line += '\n'
            file_object.write(line)

def showGetOptions():
    while True:
        option = input("\nWybierz opcje wpisujac numer: "
                       "\n 1.Dodaj studenta "
                       "\n 2.Usun studenta "
                       "\n 3. Wystaw oceny wszystkim studentom "
                       "\n 4.Wyslij emaila do studentow "
                       "\n 5.Wyswietl liste studentow"
                       "\n nr: ")

        if(int(option) >= 1 and int(option) <= 5):
            return int(option)
        else:
            print("Nie ma takiej opcji \n")

def userAddStudent(studentsList):
    print("Dodawanie studenta\n")
    email = input("podaj email: ")
    name = input("podaj imie: ")
    surname = input("podaj nazwisko: ")
    points = int(input("podaj ilosc punktow: "))

    #automatyczne ustawianie oceny
    grade = setGrade(points)
    addStudent(studentsList, email, name, surname, points, grade, 'graded')

def userDeleteStudent(studentsList):
    email = input("podaj email usuwanego studenta: ")
    deleteStudent(studentsList, email)


# Czytanie studentów z pliku formowanie każdego studenta w słownik, i dodawanie do listy
filePath = "students.txt"
students = readStudents(filePath)

#Wyswietlenie opcji i pobranie
while True:
    #pobranie numeru opcji
    option = showGetOptions()
    if option == 1:
        userAddStudent(students)
    elif option == 2:
        userDeleteStudent(students)
    elif option == 3:
        setGradesForStudents(students)
    elif option == 4:
        sendEmailToStudents(students)
        print("Wyslano wiadomosci pomyslnie")
    elif option == 5:
        showStudents(students)
    saveChangesToFile(students, "modified.txt") #roboczo zmiany są zapisywane na oddzielnym pliku



