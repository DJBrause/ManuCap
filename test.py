import random

# yathzee, je mag 2 keer opnieuw gooien

game_over = False
numberused = False
last_throw = False

score = 0
scorelist = []
nummergebruikt = False

def gooien():
    print('you rolled: ', end='')
    for d in dice:
        print(str(d) + ' ', end='')


def rerollfunction():
    reroll = input('What dice do you want to reroll?')
    print(reroll)
    reroll = reroll.split()
    print(reroll)
    for index_num, ch in enumerate(reroll):
        reroll[index_num] = int(ch) - 1
    for index_num in reroll:
        dice[index_num] = random.randint(1, 6)


#while not gameover, loop gameover = True als ronde=5
while not game_over:
    dice = []
    for d in range(5):
        dice.append(random.randint(1, 6))



    # start ronde


    #gooien functie
    gooien()
    #vraag wil je opnieuw gooien
    print('Do you want to reroll?')
    reroll = int(input('Yes = 0 , No = 1'))

    #ja
    if reroll == 0 :
        #ronde_klaar =  False
        ronde_klaar = False ##this is for further in the code
        #opnieuw gooien functie
        rerollfunction()
        #roll function
        gooien()


    #nee
    if reroll == 1 :
        #ronde_klaar True
        ronde_klaar = True ##this is for further in the code


        #dan moet je scoren
        #kiezen tussen bovenste kant of onderste kant kaart
        print('Do you want to use part 2 of the scorelist?')
        kaart = int(input('Yes = 0 , No = 1'))


        #bovenste kant
        if kaart == 1 :
            #keuze tussen 1,2,3,4,5,6,0 zodra een gekozen is voeg toe aan scorenlijst.

            while not nummergebruikt:
                optellen = int(input('Which numbers do you want to add together?'))
                nummergebruikt = True
                if optellen not in scorelist:
                    if optellen == 1 :
                        score += dice.count(1) * 1

                    elif optellen == 2 :
                        score += dice.count(2) * 2

                    elif optellen == 3 :
                        score += dice.count(3) * 3

                    elif optellen == 4 :
                        score += dice.count(4) * 4

                    elif optellen == 5 :
                        score += dice.count(5) * 5

                    elif optellen == 6 :
                        score += dice.count(6) * 6

                elif optellen in scorelist:
                #zit keuze in scorelijst
                    #print je hebt dit al gescoord, dit kan je niet scoren + scorenlijst
                    print('you already scored this number, you cant score these numbers!: ' + str(scorelist))
                    print('Choose again')
                    #print kies opnieuw
