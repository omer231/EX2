#### IMPORTS ####
import event_manager as EM

#### PART 1 ####

CURRENT_YEAR=2020
ID_LEN=8
INVALID_FIRST_DIGIT=0
MIN_AGE=16
MAX_AGE=120
MIN_SEMESTER=1
ID=0
NAME=1
AGE=2
YEAR=3
SEMESTER=4

#recives a string and if the string begins or ends with a space it removes the space
#str: the string we want to remove spaces from
def removeSpaces(str):
  return str.rstrip().lstrip()

#recives an id and returns false if the id starts with 0, contains non-number characters or is not 8 numbers long
#id: the student id
def checkId(id: str):
    if id[0]==str(INVALID_FIRST_DIGIT) or len(id)!=ID_LEN:
        return False
    if not id.isdigit():
        return False
    return True

#recives a name and returns true if the name contains only spaces and letters and false otherwise
#name: the student's name
def checkName(name: str):
    if not all(x.isalpha() or x.isspace() for x in name):
        return False
    return True

#recives the age and returns true if the age is in the valid range of numbers and false otherwise
#age: the student's age
def checkAge(age: str):
    if int(age) not in range(MIN_AGE,MAX_AGE+1):
        return False
    return True

#recives the year and returns true if the year is the correct birth year for the provided age and false otherwise
#year: the student's year of birth
def checkYear(year: str, age: str):
    if not CURRENT_YEAR-int(age)==int(year):
        return False
    return True

#recives the semster and returns true if the semster is valid and false otherwise
#semester: the semster the student is in
def checkSemester(semester: str):
    if int(semester) < MIN_SEMESTER:
        return False
    return True

#recives a dictionary which represents a student registration to the event
#row: the dictionary containing the info about the regestration
def checkRow(row):
    if checkId(row["id"]) and checkName(row["name"]) and checkAge(row["age"]) and checkYear(row["year"], row["age"]) and checkSemester(row["semester"]):
        return True
    return False

#prints the data in the dictionary to a string
#row: the dictionary containing the info about the regestration
def rowToStr(row: str):
    return row["id"]+", "+row["name"]+", "+row["age"]+", "+row["year"]+", "+row["semester"]+"\n"

#recives a path for to a file and returns a string containing the file's contents
#path: the path to the desired file
def fileToStr(path: str):
    return open(path, "r").read()

#recives a string containing the contents of the file
#returns the contents of the file sorted by id into an array
#str: the string with the contents of the file
def strToRows(str: str):
    lines=str.split("\n")
    rows=[]
    for i in range(0, len(lines)):
        filtered=' '.join(lines[i].split()).split(',')
        if filtered[ID]!='':
            rows.append({"id": removeSpaces(filtered[ID]),
            "name": removeSpaces(filtered[NAME]),
            "age": removeSpaces(filtered[AGE]),
            "year": removeSpaces(filtered[YEAR]),
            "semester": removeSpaces(filtered[SEMESTER])})
    return sorted(rows, key = lambda i: i["id"])

#recives the path to a file and filters out the invalid registrations
#returns an array with the valid registratins in the required order
#orig_file_path: the fath to the desired file
def rowsCorrect(orig_file_path: str):
    rows=strToRows(fileToStr(orig_file_path))
    rows_id_duplicates=[]
    for i in range(0, len(rows)): 
        row=rows[i]  
        if checkRow(row):
            rows_id_duplicates.append(row)
    rows_correct=[]
    for i in range(0, len(rows_id_duplicates)-1): 
        row=rows_id_duplicates[i]
        next_row=rows_id_duplicates[i+1]   
        if row["id"]!=next_row["id"]:
            rows_correct.append(row)
    if len(rows_id_duplicates)>0:
        rows_correct.append(rows_id_duplicates[len(rows_id_duplicates)-1])
    return rows_correct

#recives the path to a file and filters out the invalid registrations and prints them to a string
#orig_file_path: the fath to the desired file
def strCorrect(orig_file_path: str):
    str_correct=""
    rows_correct=rowsCorrect(orig_file_path)
    for i in range(0, len(rows_correct)): 
       str_correct+=rowToStr(rows_correct[i])
    return str_correct

# Filters a file of students' subscription to specific event:
#   orig_file_path: The path to the unfiltered subscription file
#   filtered_file_path: The path to the new filtered file
def fileCorrect(orig_file_path: str, filtered_file_path: str):
    str_correct=strCorrect(orig_file_path)
    file=open(filtered_file_path, "w")
    file.write(str_correct)
    file.close()

# Using a file with students, the function creates a list containing dictionaries, a dictionary per student, with id, name and age
#   in_fie_path: The path to the file of students
def createListWithStudents(in_file_path: str):
    file_in = open(in_file_path, "r")
    students = []
    for line in file_in:
        id = line.split(',')[0].strip()
        name = line.split(',')[1].strip()
        age = line.split(',')[2].strip()
        year = line.split(',')[3].strip()
        semester = line.split(',')[4].strip()
        d = {"id":id,"name":name, "age":age, "year":year, "semester":semester}
        students.append(d)
    file_in.close()
    return students

# Returns the "id" key from dictionary of student as int
def getIdFromList(student):
    return int(student.get("id"))

# Returns the "name" key from dictionary of student as int
def getAgeFromList(student):
    return int(student.get("age"))

# Sorts the list, first by id and then by age (so if several students have the same age, the lower id is the earlier student in the list)
def sortStudentListByAge(students: list):
    students.sort(key=getIdFromList)
    students.sort(key=getAgeFromList)

#@@@@@@@@@@@@@@@@@@@@@@@@

# Writes the names of the K youngest students which subscribed 
# to the event correctly.
#   in_file_path: The path to the unfiltered subscription file
#   out_file_path: file path of the output file
def printYoungestStudents(in_file_path: str, out_file_path: str, k: int) -> int:
    if k < 1:
        return -1
    students = createListWithStudents(in_file_path)
    sortStudentListByAge(students)
    cnt = 0
    file_out = open(out_file_path, "w")
    for item in students:
        if k > 0:
            file_out.write(item["name"] + "\n")
            cnt += 1
            k -= 1
    return cnt
    
# Calculates the avg age for a given semester
#   in_file_path: The path to the unfiltered subscription file
#   retuns the avg, else error codes defined.
def correctAgeAvg(in_file_path: str, semester: int) -> float:
    if semester < 1:
        return -1
    students = createListWithStudents(in_file_path)
    sum = 0
    cnt = 0
    for item in students:
        if int(item["semester"]) == semester:
            sum += int(item["age"])
            cnt += 1
    if cnt == 0:
        return 0
    return sum/cnt
    

#### PART 2 ####
# Use SWIG :)

## MY HELPER FUNCTIONS ##
# Returns the earliest date in the list
#   events: the list containing events and their dates
def findEarliestDate (events :list):
    list_len = len(events)
    if list_len != 0:
        min_date = events[0]["date"]
        i = 0
        while list_len > 0:
            result = EM.dateCompare(min_date, events[i]["date"])
            if result > 0:
                min_date = events[i]["date"]
            i += 1
            list_len -= 1
        return min_date
    return -1

# Inserts all events in the list to the event manager
#   events: the list containing the events
#   event_manager: contains the events
def insertAllEvents (events :list, event_manager):
    list_len = len(events)
    i = 0
    while list_len > 0:
        event_name = events[i]["name"]
        event_id = events[i]["id"]
        event_date = events[i]["date"]
        result = EM.emAddEventByDate(event_manager, event_name, event_date, event_id)
        list_len -= 1
        i += 1


## FUNCTION TO WRITE ##
# print the events in the list "events" using the functions from hw1
#   events: list of dictionaries
#   file_path: file path of the output file
def printEventsList(events :list,file_path :str): #em, event_names: list, event_id_list: list, day: int, month: int, year: int):
    start_date = findEarliestDate(events)
    event_manager = EM.createEventManager(start_date)
    insertAllEvents(events, event_manager)
    EM.emPrintAllEvents(event_manager, file_path)
    return event_manager
    
    
def testPrintEventsList(file_path :str):
    events_lists=[{"name":"New Year's Eve","id":1,"date": EM.dateCreate(30, 12, 2020)},\
                    {"name" : "annual Rock & Metal party","id":2,"date":  EM.dateCreate(21, 4, 2021)}, \
                                 {"name" : "Improv","id":3,"date": EM.dateCreate(13, 3, 2021)}, \
                                     {"name" : "Student Festival","id":4,"date": EM.dateCreate(13, 5, 2021)},    ]
    em = printEventsList(events_lists,file_path)
    for event in events_lists:
        EM.dateDestroy(event["date"])
    EM.destroyEventManager(em)

#### Main #### 
# feel free to add more tests and change that section. 
# sys.argv - list of the arguments passed to the python script
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        #testPrintEventsList(sys.argv[1])
        r = printYoungestStudents(sys.argv[1], "out.txt", 1)
        print(correctAgeAvg(sys.argv[1],3))
