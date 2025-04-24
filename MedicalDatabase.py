import mysql.connector
from mysql.connector import errorcode



# Password for the SQL server is stored on a .txt file in the same folder as the python script
# No, this is not secure, but I'd rather not put any sensitive information in my source code either.
f = open("password.txt", "r")
p = f.read()
try:
    cnx = mysql.connector.connect(user='root' , password=p, host='127.0.0.1')
    cursor = cnx.cursor()
    cursor.execute('USE MedicalDatabase')
    command = 0
    while(command != "EXIT"):
        print("Input your next command. (Type EXIT to exit)")
        command = input()
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
