import random as r
import os
def clr():
    os.system('cls')
random_wordlist= ['rainbow', 'computer', 'science', 'programming','python', 'mathematics', 'player', 'condition','reverse', 'water', 'board', 'geeks']
user_choice_count=1
clr()
randchoice=r.choice(random_wordlist)
name = input("What is your name\t? ")
print("Good Luck ! \t", name)
while user_choice_count<=7:
    try:
        entered_choice=input(f'Enter your {user_choice_count} guess \t')
        if entered_choice.lower() == randchoice:
            print(f'Congrats you guessed it right on {user_choice_count} , The word was {randchoice}')
            break
        elif(entered_choice.lower()!= randchoice and user_choice_count==7):
            print("You Loose")
            print(f'Word was {randchoice}')
            break
        else:
            print(f'Incorrect you have {7-user_choice_count} guesses')
            print('Try again')
            user_choice_count=user_choice_count+1
    except:
        print('Error try again ')
    
