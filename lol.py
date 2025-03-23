import random as r
import os 
def cl():
    os.system('cls')
rizz_lines = [
    "Wanna be Minecraft without the craft?",
    "Are you French? Because Eiffel for you.",
    "Do you like science? Because I got my ion you.",
    "Are you German? Because I’d like to be Ger-man.",
    "Are you a keyboard? Because you’re just my type.",
    "Are you a fruit? Because you look like a FINE-apple!",
    "Do you play soccer? Because you look like a keeper.",
    "Is your name Wi-Fi? Because I’m feeling a connection.",
    "Do you like Nintendo? Because Wii look good together.",
    "Are you a cannon? Because you’ve just blown me away.",
    "Are you a time traveler? Because I see you in my future!",
    "Do you have a map? Because I just got lost in your eyes.",
    "Is your birthday on October 10th? Because you’re a 10/10.",
    "I see you like vodka. Does that mean you’ll give me a shot?",
    "On a scale of 1 to America, how free are you this weekend?",
    "Hey, my name’s Microsoft. Can I crash at your place tonight?",
    "Is your license suspended? Because you’re driving me crazy!",
    "Are you my laptop? Because you’re really hot and I’m concerned.",
    "Are you a supernova? Because you’re out-of-this-world attractive!",
    "Is your name John? Because I’ve never Cena prettier girl than you.",
    "Didn’t we have a class together? I could’ve sworn we had chemistry!",
    "Have you been to the doctor lately? I think you’re lacking in vitamin me.",
    "Are you my student loans? Because I want you around for the rest of my life.",
    "Can I follow you on Instagram? My mom always told me to follow my dreams.",
    "Are you my appendix? Because I have this feeling in my stomach like I want to take you out."
]
cl()
today_rizz=yesterday_rizz=r.choice(rizz_lines)
x=0
while True:
    print ('Welcome to Rizzly :')
    while today_rizz==yesterday_rizz:
        today_rizz=r.choice(rizz_lines)
    yesterday_rizz=today_rizz
    print(f'Todays Rizz:\t{today_rizz}')
    x=int(input(('for more rizz enter anything to exit enter 2\t')))
    if x==1:
        continue
    elif x==2:
         exit(0)
         