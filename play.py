from keras.models import load_model
import cv2
import numpy as np
from random import choice
import pygame
import time
import random

pygame.init()

#
#sounds
#
bgm = pygame.mixer.music.load("n-sounds\Bgm.wav")
end = pygame.mixer.Sound("m-sounds\khatam.wav")

tie = pygame.mixer.Sound("n-sounds\\tie.wav")

start = pygame.mixer.Sound("m-sounds\ShurKarteH.wav")
padh = pygame.mixer.Sound("m-sounds\Padhai.wav")

#lose
lose = pygame.mixer.Sound("n-sounds\lose.wav")
abey = pygame.mixer.Sound("m-sounds\AbeySale.wav")

#win
win = pygame.mixer.Sound("n-sounds\win.wav")
sabbas = pygame.mixer.Sound("m-sounds\ShabasBeta.wav")



play = "yes"

count1 = 0
count2 = 0

check = 0

def startPlay():
    num = random.randint(0,1)
    if num == 0:
        start.play()
    if num == 1:
        padh.play()

startPlay()

REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}

def losePlay():
    num = random.randint(0,1)
    if num == 0:
        win.play()
    if num == 1:
        sabbas.play()

def winPlay():
    num = random.randint(0,1)
    if num == 0:
        lose.play()
    if num == 1:
        abey.play()



def mapper(val):
    return REV_CLASS_MAP[val]


def calculate_winner(move1, move2):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissors":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"


model = load_model("rock-paper-scissors-model.h5")

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

prev_move = None

pygame.mixer.music.play(-1)
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # rectangle for user to play
    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
    # rectangle for computer to play
    cv2.rectangle(frame, (800, 100), (1200, 500), (255, 255, 255), 2)

    

    # extract the region of image within the user rectangle
    roi = frame[100:500, 100:500]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))

    # predict the move made
    pred = model.predict(np.array([img]))
    move_code = np.argmax(pred[0])
    user_move_name = mapper(move_code)

    # predict the winner (human vs computer)
    if prev_move != user_move_name:
        if user_move_name != "none":
            if play == "yes":
                computer_move_name = choice(['scissors','rock','paper'])
                winner = calculate_winner(user_move_name, computer_move_name)
                
                #playing sounds
                if user_move_name == "rock":
                    play = "no"
                    user = user_move_name
                    comp = computer_move_name
                    won = winner
                    if computer_move_name == "scissors":
                        win.play()
                        count1 +=1
                    if computer_move_name == "paper":
                        lose.play()
                        count2 += 1
                    if computer_move_name == "rock":
                        tie.play()    
                        

                if user_move_name == "scissors":
                    play = "no"
                    user = user_move_name
                    comp = computer_move_name
                    won = winner
                    if computer_move_name == "paper":
                        win.play()
                        count1 += 1    
                    if computer_move_name == "rock":
                        lose.play()
                        count2 += 1
                    if computer_move_name == "scissors":
                        tie.play()
                    
                if user_move_name == "paper":
                    play = "no"
                    user = user_move_name
                    comp = computer_move_name
                    won = winner
                    if computer_move_name == "rock":
                        win.play()
                        count1 += 1 
                    if computer_move_name == "scissors":
                        lose.play()
                        count2 += 1   
                    if computer_move_name == "paper":
                        tie.play()
            
        else:
            computer_move_name = "none"
            winner = "none"
            play = "yes"
    prev_move = user_move_name

    #text
    def showText():
        cv2.putText(frame, str(count1),
                    (100, 800), font, 2, (0,255,255), 4, cv2.LINE_AA)
        cv2.putText(frame, str(count2),
                    (800, 800), font, 2, (127,255,0), 4, cv2.LINE_AA)
        
        #score
        if count1 - count2 <=0:
            cv2.putText(frame, "to win, you should have 5 points more than comp",
                       (10, 700), font, 1.5, (13,13,13), 3, cv2.LINE_AA)
        else:
            if count1 != 0:
                cv2.putText(frame, "+"+str(5 -(count1 - count2))+"to win",
                        (10, 700), font, 1.5, (13,13,13), 3, cv2.LINE_AA)

        #winner
        if winner == "User":
            cv2.putText(frame, "Winner: " + "User",
                    (400, 600), font, 2, (0,255,255), 4, cv2.LINE_AA)
        if winner == "Computer":
            cv2.putText(frame, "Winner: " + "Computer",
                    (400, 600), font, 2, (127,255,0), 4, cv2.LINE_AA)
        if winner == "Tie":
            cv2.putText(frame, "Winner: " + "Tie",
                    (400, 600), font, 2, (255,64,64), 4, cv2.LINE_AA)
        if winner == "none":
            cv2.putText(frame, "Winner: " + "Waiting...",
                    (400, 600), font, 2, (252,230,201), 4, cv2.LINE_AA)


    # display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    if play == "yes":
        cv2.putText(frame, "Your Move: " + user_move_name,
                    (50, 50), font, 1.2, (0,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Computer's Move: " + computer_move_name,
                    (750, 50), font, 1.2, (127,255,0), 2, cv2.LINE_AA)
        
        showText()
        
    else:
        showText()
        cv2.putText(frame, "Your Move: " + user,
                    (50, 50), font, 1.2, (0,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Computer's Move: " + comp,
                    (750, 50), font, 1.2, (127,255,0), 2, cv2.LINE_AA)
        cv2.putText(frame, "remove your hand then play again",
                    (100, 900), font, 2, (0, 0, 255), 4, cv2.LINE_AA)
        
              

        icon = cv2.imread(
            "images/{}.png".format(comp))
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon

    if computer_move_name != "none":

        icon = cv2.imread(
            "images/{}.png".format(computer_move_name))
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon

    cv2.imshow("Rock Paper Scissors", frame)

    if count1 == count2 + 5:
        play="no"
        end.play()
        time.sleep(1.5)
        break

    k = cv2.waitKey(10)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
