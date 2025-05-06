import mysql.connector
from mysql.connector import errorcode
import re









def add_prescription(cursor):
  print("Who is the prescription for?")
  command = "blank"
  command = input()
  try:
    cursor.execute("SELECT PATIENT.P_id FROM PATIENT WHERE PATIENT.P_Name = '"+ command + "'")
    id = re.sub("[^0-9]","",str(cursor.fetchone()))
    if (len(id) == 0):
      print("Patient not found.")
      return
  except mysql.connector.Error as err:
    print(err)
    return
  
  medicine_name = "blank"
  print("What is the type of medicine?")
  medicine_name = input()

  dosage = "blank"
  print("What is the dosage?")
  dosage = input()

  frequency = "blank"
  print("What is the frequency of the medicine?")
  frequency = input()

  print("Are you sure this is the correct information? (YES or NO)\nPatient: " + command + "\nMedication: " + medicine_name +"\nDosage: " + dosage +"\nFrequency: " + frequency)
  confirmed = "blank"
  confirmed = input()
  if(confirmed.upper() == "YES"):
    try:
      cursor.execute("INSERT INTO MEDICATIONS VALUES("+ id +", '"+ medicine_name +"', '"+ frequency +"', '"+ dosage +"');")
      #print("Ran command : INSERT INTO MEDICATIONS VALUES("+ id +", '"+ medicine_name +"', '"+ frequency +"', '"+ dosage +"');")
      print("Medication successfully prescribed to patient named " + command)
      cursor.commit()
    except mysql.connector.Error as err:
      print(err)
      prescription(cursor)
      return
  else:
    print("Action terminated.")
    return
  return
  

  
  




def prescription(cursor):
   c = "blank"

   command = "blank"
   while(command.upper()!= "EXIT"):
    print("Would you like to VIEW, ADD, or RENEW prescriptions? (Type BACK to return)")
    c = input()
    match c.upper():
      case "VIEW":
        try:
          cursor.execute("""
                     SELECT MEDICATIONS.Medication_name, PATIENT.P_Name
                     FROM PATIENT
                     CROSS JOIN MEDICATIONS
                     WHERE MEDICATIONS.P_id = PATIENT.P_id
                     """)
          myresult = cursor.fetchall()
          for x in myresult:
            print(x)
        except mysql.connector.Error as err:
          print(err)
      case "ADD":
        add_prescription(cursor)
      case "BACK":
         return
      case "EXIT":
        return
    
      
      
   

# Password for the SQL server is stored on a .txt file in the same folder as the python script
# No, this is not secure, but I'd rather not put any sensitive information in my source code.
f = open("password.txt", "r")
p = f.read()
try:
    cnx = mysql.connector.connect(user='root' , password=p, host='127.0.0.1')
    cursor = cnx.cursor()
    cursor.execute('USE MedicalDatabase')
    command = "blank"
    while(command.upper()!= "EXIT"):
        print("Input your next command. (Type EXIT to exit) (Type HELP for a list of commands)")
        command = input()
        match command.upper():
            case "HELP":
              print("\"EXIT\" - Exits the application.\n" \
              "\"HELP\" - Lists all available commands.\n" \
              "\"PRESCRIPTION\" or \"P\" - Provides options to view, add, or renew prescriptions for patients.")
            case "P":
              prescription(cursor)
            case "PRESCRIPTION":
              prescription(cursor)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    cnx.close()
f.close()
