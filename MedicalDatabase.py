import mysql.connector
from mysql.connector import errorcode







def prescription(cursor):
   print("Would you like to VIEW, ADD, or RENEW prescriptions? (Type BACK to return)")
   c = "blank"

   command = "blank"
   while(command.upper()!= "EXIT"):
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
        
      case "BACK":
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
