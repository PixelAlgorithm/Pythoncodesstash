import random as r
import os
def cl():
    os.system('acls')


word_list=['apple', 'banana', 'mango','strawberry',
'orange', 'grape', 'pineapple', 'apricot' ,'lemon','coconut', 'watermelon' ,
'cherry' ,'papaya' ,'berry','peach', 'lychee' ,'muskmelon']
picked_string=r.choice(word_list)
chances=len(picked_string)+2
print(picked_string,chances)
guess_count=0
picked_list=list(picked_string)
entered_list=['_']*len(picked_string)
entered_string=''
while guess_count<chances:
    if entered_string==picked_string:
        print('Congrats You won ')
        exit(0)
        guess_count=guess_count-1
    guess_count=guess_count+1
    for i in entered_list:
       print(i,end=' ')
    print() 
    ###cl()
    entered_character=input(f'Enter your {guess_count} guess \t')
    temp=0
    for i in range(len(picked_list)):
        #print(picked_list[i])
        if(picked_list[i] == entered_character):
            entered_list[i]=entered_character
            print('Correct')
            temp=1
    if(temp!=1):
        print('Wrong guess')
    entered_string=''
    for i in entered_list:
        entered_string=entered_string+i
        #print(entered_string)
print (f'You lose \n The word was {picked_string} ')
