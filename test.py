import cv2
import pytesseract
import mysql.connector

image=cv2.imread('temp1.jpeg')
gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

canny_edge=cv2.Canny(gray_image,170,200)

contours,new=cv2.findContours(canny_edge.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours,key=cv2.contourArea,reverse=True)[:30]

contour_with_license_plate=None
license_plate=None
x=None
y=None
w=None
h=None

for contour in contours:
	perimeter=cv2.arcLength(contour,True)
	approx=cv2.approxPolyDP(contour,0.01*perimeter,True)
	if len(approx)==4:
		contour_with_license_plate=approx
		x,y,w,h = cv2.boundingRect(contour)
		license_plate=gray_image[y:y+h,x:x+w]
		break

license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
(thresh, license_plate) = cv2.threshold(license_plate, 150, 180, cv2.THRESH_BINARY)

#Text Recognition
text = pytesseract.image_to_string(license_plate,lang='eng',config="--psm 7")
#Draw License Plate and write the Text
image = cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 3)
image = cv2.putText(image, text, (x-100,y-50), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6, cv2.LINE_AA)

print("License Plate :", text)

cv2.imshow("License Plate Detection",image)
cv2.waitKey(0)

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="phantom",
  password="Phantom@1402",
  database="sps"
)

mycursor = mydb.cursor()

# Check the details of the Vehicle Owner
sql = "SELECT * FROM faculty WHERE Registration_Number = %s"
y=('ZG 3254-D',)
mycursor.execute(sql, y)
myresult1 = mycursor.fetchall()
for x in myresult1:
  print(x)
sql2 = "UPDATE parkslots SET allotedsap = (SELECT SAP FROM faculty WHERE faculty.Registration_Number = %s) WHERE status='AVAILABLE' LIMIT 1"
mycursor.execute(sql2, y)
sql3 = "UPDATE parkslots SET status='BOOKED' WHERE allotedsap IS NOT NULL"
sql4 = "SELECT * FROM parkslots"
mycursor.execute(sql3)
mycursor.execute(sql4)
myresult2 = mycursor.fetchall()
for x in myresult2:
  print(x)
