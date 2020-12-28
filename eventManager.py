#### IMPORTS ####
#import event_manager as EM

#### PART 1 ####
# Filters a file of students' subscription to specific event:
#   orig_file_path: The path to the unfiltered subscription file
#   filtered_file_path: The path to the new filtered file

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

def removeSpaces(str):
  return str.rstrip().lstrip()

def checkId(id: str):
    if id[0]==str(INVALID_FIRST_DIGIT) or len(id)!=ID_LEN:
        return False
    if not id.isdigit():
        return False
    return True

def checkName(name: str):
    if not all(x.isalpha() or x.isspace() for x in name):
        return False
    return True

def checkAge(age: str):
    if int(age) not in range(MIN_AGE,MAX_AGE+1):
        return False
    return True

def checkYear(year: str, age: str):
    if not CURRENT_YEAR-int(age)==int(year):
        return False
    return True

def checkSemester(semester: str):
    if int(semester) < MIN_SEMESTER:
        return False
    return True

def checkRow(row):
    if checkId(row["id"]) and checkName(row["name"]) and checkAge(row["age"]) and checkYear(row["year"], row["age"]) and checkSemester(row["semester"]):
        return True
    return False

def rowToStr(row: str):
    return row["id"]+", "+row["name"]+", "+row["age"]+", "+row["year"]+", "+row["semester"]+"\n"

def fileToStr(path: str):
    return open(path, "r").read()

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

def strCorrect(orig_file_path: str):
    str_correct=""
    rows_correct=rowsCorrect(orig_file_path)
    for i in range(0, len(rows_correct)): 
       str_correct+=rowToStr(rows_correct[i])
    return str_correct

def fileCorrect(orig_file_path: str, filtered_file_path: str):
    str_correct=strCorrect(orig_file_path)
    file=open(filtered_file_path, "w")
    file.write(str_correct)
    file.close()

fileCorrect("/home/omer.aboudy/mtm/ex2/tests/input", "/home/omer.aboudy/mtm/ex2/tests/myout")
    
# Writes the names of the K youngest students which subscribed 
# to the event correctly.
#   in_file_path: The path to the unfiltered subscription file
#   out_file_path: file path of the output file
def printYoungestStudents(in_file_path: str, out_file_path: str, k: int) -> int:
    pass
    #TODO
    
    
# Calculates the avg age for a given semester
#   in_file_path: The path to the unfiltered subscription file
#   retuns the avg, else error codes defined.
def correctAgeAvg(in_file_path: str, semester: int) -> float:
    pass
    #TODO
    

#### PART 2 ####
# Use SWIG :)
# print the events in the list "events" using the functions from hw1
#   events: list of dictionaries
#   file_path: file path of the output file
def printEventsList(events :list,file_path :str): #em, event_names: list, event_id_list: list, day: int, month: int, year: int):
    pass
    #TODO   
    
    
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
        testPrintEventsList(sys.argv[1])
