import mysql.connector

f = open("password.txt", "r")
print(f.read())
p = f.read().rstrip()
#print(p)
cnx = mysql.connector.connect(user='root', password=p , host='localhost')
cnx.close()
f.close()
