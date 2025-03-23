from IPython.display import clear_output
from random import randint
def display(a=[]):
    print(f"Player 1:{p1}      Player2:{p2}")
    print(f"|{a[7]}     |     {a[8]}     |       {a[9]}|")
    print('---------------------------------')
    print(f"|{a[4]}     |     {a[5]}     |       {a[6]}|")
    print('---------------------------------')
    print(f"|{a[1]}     |     {a[2]}     |       {a[3]}|")
    print('---------------------------------')
def pm(board, marker, posn):
    board[pos] = marker
def inputz():
    clear_output()
    ch='Wong'
    df=['X','O']
    print("Hello Welcome to my game")
    while ch not in df:
        ch=input("Player 1 , Choose X or O")
        if ch not in df:
            clear_output()
            print('Invalid choice !!')
    
    if ch=='X':
        return ('X','O')
    else:
        return('O','X')
def wc(board,mark):
    
    return ((board[7] == mark and board[8] == mark and board[9] == mark) or 
    (board[4] == mark and board[5] == mark and board[6] == mark) or 
    (board[1] == mark and board[2] == mark and board[3] == mark) or 
    (board[7] == mark and board[4] == mark and board[1] == mark) or 
    (board[8] == mark and board[5] == mark and board[2] == mark) or 
    (board[9] == mark and board[6] == mark and board[3] == mark) or 
    (board[7] == mark and board[5] == mark and board[3] == mark) or 
    (board[9] == mark and board[5] == mark and board[1] == mark))
import random
def plays():
    if random.randint(0,2) == 1:
        return 'Player 1'
    else:
        return 'Player 2'
def sc(board,pos):
    return (board[pos] == ' ')
def pc(board):
    position = 0
    
    while position not in [1,2,3,4,5,6,7,8,9] or not sc(board, position):
        position = int(input('Choose your next position: (1-9) '))
        
    return position

def fc(board):
    for i in range(1,10):
        if sc(board,i):
            return False
    return True
def restartz():
  return(input('Do you want to play again? Enter Yes or No: ').lower().startswith('y'))
while True:
    tb=[' ']*10
    g =True
    p1,p2=inputz()
    turn=plays()
    print (p1 , p2)
    while g:
        if turn == 'Player 1':
            clear_output()
            display(tb)
            pos=pc(tb)
            pm(tb,p1,pos)
            if wc(tb,p1):
                clear_output()
                print ("Player 1 Wins ")
                display(tb)
                g=False
            else:
                 if fc(tb):
                        clear_output()
                        print("Draw")
                        display(tb)
                        break
                 else:
                     turn='Player 2'
        else:
            clear_output()
            display(tb)
            pos=pc(tb)
            pm(tb,p2,pos)
            if wc(tb,p2):
                clear_output()
                print ("Player 2 Wins ")
                display(tb)
                g=False
            else:
                if fc(tb):
                    clear_output()
                    print("Draw")
                    display(tb)
                    break
                else:
                    turn='Player 1'
    if not restartz():
        break