import mysql.connector
from mysql.connector import errorcode
import re






# Function for renewing a patient's prescription.
def renew_prescription(cnx):
  cursor = cnx.cursor()
  print("What is the patient's name?")
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
  print("Which prescription is being renewed?")
  command = input()
  try:
    cursor.execute("SELECT MEDICATIONS.Medication_name FROM MEDICATIONS WHERE MEDICATIONS.P_id = "+ id + " AND MEDICATIONS.Medication_name = '" + command +"';")
    medicationName = re.sub(r"[^a-zA-Z0-9\s]", '', str(cursor.fetchone()))
    print(medicationName)
    if (medicationName == "None"):
      print("Prescription not found.")
      return
  except mysql.connector.Error as err:
    print(err)
    return
  print("What is the new dosage?")
  dosage = input()
  print("What is the new frequency the medicine should be taken?")
  frequency = input()
  
  try:
    cursor.execute("DELETE FROM MEDICATIONS WHERE MEDICATIONS.P_id = "+id+" AND MEDICATIONS.Medication_name = '"+ medicationName +"';")
    cursor.execute("INSERT INTO MEDICATIONS VALUES("+ id +", '"+ medicationName +"', '"+ frequency +"', '"+ dosage +"');")
    cnx.commit()
    print(medicationName + " prescription for " + command + " has been renewed.")
  except mysql.connector.error as err:
    print(err)
    return









# Function for adding a prescription.
def add_prescription(cnx):
  cursor = cnx.cursor()
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
      print("Medication successfully prescribed to patient named " + command)
      cnx.commit()
    except mysql.connector.Error as err:
      print(err)
      prescription(cnx)
      return
  else:
    print("Action terminated.")
    return
  return
  

  
  



# Function that opens the prescription command menu.
def prescription(cnx):
   cursor = cnx.cursor()
   c = "blank"

   command = "blank"
   while(command.upper()!= "EXIT"):
    print("Would you like to VIEW, ADD, or RENEW prescriptions? (Type BACK or EXIT to return)")
    c = input()
    match c.upper():
      case "VIEW":
        try:
          cursor.execute("""
                     SELECT MEDICATIONS.Medication_name, PATIENT.P_Name, MEDICATIONS.Frequency, MEDICATIONS.Dosage
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
        add_prescription(cnx)
      case "RENEW":
        renew_prescription(cnx)
      case "BACK":
         return
      case "EXIT":
        return



# Function that opens the billing command menu.
def billing(cnx):
  cursor = cnx.cursor()
  c = "blank"
  while(c.upper != "EXIT"):
    print("Would you like to ADD or VIEW bills? (Type BACK or EXIT to return)")
    c = input()
    match c.upper():
      case "VIEW":
        try:
          cursor.execute("""
                     SELECT BILLING.B_id, PATIENT.P_Name, BILLING.Due_date, BILLING.Total_owed, BILLING.Amount_paid
                     FROM BILLING
                     CROSS JOIN PATIENT
                     WHERE BILLING.P_id = PATIENT.P_id
                     """)
          myresult = cursor.fetchall()
          print("(Bill ID, Patient Name, Due Date, Total Owed, $ Paid)")
          for x in myresult:
            print(x)
        except mysql.connector.Error as err:
          print(err)
      case "ADD":
        add_bill(cnx)
      case "EXIT":
        return
      case "BACK":
        return
      


# Function for adding a bill.
def add_bill(cnx):
  cursor = cnx.cursor()
  print("Enter the patient's ID")
  command = input()
  try:
    cursor.execute("SELECT PATIENT.P_id FROM PATIENT WHERE PATIENT.P_id = "+ command+";")
    id = re.sub("[^0-9]","",str(cursor.fetchone()))
    if (len(id) == 0):
      print("Patient not found.")
      return
  except mysql.connector.Error as err:
    print(err)
    return
  
  print("Enter a new bill ID. (6 digits)")
  bill_id = input()
  print("Enter the due date. (Year-Month-Day XXXX-XX-XX)")
  date = input()
  print("Enter the amount of money owed")
  owed = input()

  print("Are you sure this is the correct information? (YES or NO)\n" \
        "Patient ID: " + id + "\n" \
        "New Bill ID: " + bill_id + "\n" \
        "Due Date: " + date + "\n" \
        "Amount Owed: " + owed)
  confirmation = input()
  match confirmation.upper():
    case "YES":
      try:
        cursor.execute("INSERT INTO BILLING VALUES("+ bill_id +", "+ id +", '"+ date +"', "+ owed + ", 0.00);")
        cursor.execute("INSERT INTO OWES VALUES("+ id + ", " + bill_id + ");")
        print("Bill successfully added.")
        cnx.commit()
      except mysql.connector.Error as err:
        print(err)
        return
    case "NO" :
      print("Action terminated")
      return
  return





# Password for the SQL server is stored on a .txt file in the same folder as the python script.
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
              "\"PRESCRIPTION\" or \"P\" - Provides options to view, add, or renew prescriptions for patients.\n" \
              "\"BILLING\" or \"BILL\" or \"B\" - Provides options to view or add bills.")
            case "P":
              prescription(cnx)
            case "PRESCRIPTION":
              prescription(cnx)
            case "BILLING":
              billing(cnx)
            case "BILL":
              billing(cnx)
            case "B":
              billing(cnx)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    cnx.commit()
    cnx.close()
f.close()
