import random, time

def generateNum():
    return str(random.randint(1000, 10000))


randomNum = generateNum()

#Statistics
games = 1
currentTrials = 1
currentBulls = 0
currentCows = 0

#time on each game
start = 0
end = 0

print("\n\nGAME " + str(games) + " | Random number: " + randomNum)
print("Guess the number of 4 digits")

start = time.time()

while True:

    guess = input("Enter your guess: ")

    if guess.lower() == "exit":
        print("Exiting the game...")
        exit(0)

    if guess == randomNum:

        end = time.time()

        print("Congratulations! You guessed the number after " + str(currentTrials)  + " trials in " + str(round(end-start,1)) + " seconds!")
        print("Cows/Trial: " + str(currentCows/currentTrials) + " Bulls/Trial: " + str(currentBulls/currentTrials) + "\n\n")
        print("Starting a new game...")
        randomNum = generateNum()
        games+=1
        currentTrials = 1
        print("\n\nGAME " + str(games) + " | Random number: " + randomNum)
        start = time.time()
    else:
        cows = 0
        bulls = 0
        correctPositions = []#The numbers that are in the correct position are ignored when checking for cows
        usedCowPositions = []#When checking for cows, we dont use the same in the random number more than once
        # Check for bulls
        for i in range(0,4):
            if guess[i] == randomNum[i]:
                bulls += 1
                correctPositions.append(i)


        #Check for cows:
        for i in range(0,4):
            if i not in correctPositions:
                for j in range(0,4):
                    if j not in usedCowPositions and j not in correctPositions:
                        if guess[i] == randomNum[j]:
                            cows += 1
                            usedCowPositions.append(j)
                            break

        print("Cows: " + str(cows) + " Bulls: " + str(bulls))
        currentTrials += 1
        currentCows+=cows
        currentBulls+=bulls