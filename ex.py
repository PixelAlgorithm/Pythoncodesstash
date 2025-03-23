#Project game
import random
name=input("Enter your name \n") 
print(f"Welcome {name} To My Game ")
balance=0
print (f"Your balance :{balance}")
while True:
 c=input("Enter 1 to add a dollar Enter 2 to view balance and Enter 3 to exit from playing")
 c=float(c)
 try:
  if(c==1):
      balance=balance+1
  elif(c==2):
     print(balance)
  elif(c==3):
     print("Exiting")
     break
  else:
     print("Enter a valid choice")
 except:
     print("Enter numbers from 1 to 2")
exit()
