import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="phantom",
  password="Phantom@1402",
  database="sps"
)

mycursor = mydb.cursor()

# Check the details of the Vehicle Owner
sql = "SELECT * FROM faculty WHERE Registration_Number = %s"
y = ("RJ01CD0444",)
mycursor.execute(sql, y)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# Update the details in the Slots Table
#sql1 = "SELECT SAP FROM faculty AS sapid WHERE Registration_Number = %s"
#y = ("RJ01CD0444",)
#mycursor.execute(sql1, y)
sql2 = "UPDATE parkslots SET allotedsap = (SELECT SAP FROM faculty WHERE faculty.Registration_Number = %s) WHERE parkslotid='A1' OR parkslotid='A2' OR parkslotid='A3'"
mycursor.execute(sql2, y)
sql3 = "UPDATE parkslots SET status='BOOKED' WHERE allotedsap IS NOT NULL"
sql4 = "SELECT * FROM parkslots"
mycursor.execute(sql3)
mycursor.execute(sql4)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)
