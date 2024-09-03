#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>
#include <signal.h>
#include <bits/sigaction.h>
#include <asm-generic/signal-defs.h>

#define FIFOFILE "ex2Fifo"
#define WORDLENGTH 300
#define PLAYERS 4

//The word to be distorted
char* word;

//Applies distortion algorithm on given word
void distortWord(int maxNumVowels){


    int length = strlen(word);
    char* newWord = (char*)malloc(WORDLENGTH * sizeof(char));

    //Seeding the random number generator based on the current time and the process ID
    srand(time(NULL) ^ getpid());

    //Generating a random number (0 or 1) to decide which distortion algorithm to use
    int random = rand() % 2;

    //0 is for chicken language, 1 is for no distortion
    if (random == 0){

        //Number of vowels found in this call of the function
        int foundVowels =0;
        
        //The true index at which we added a letter to the distorted word
        int v = 0;

        //Iterating through the characters of the given word to create the newly distorted word
        for (int i = 0; i < length; i++){

            char tempLetter = tolower((unsigned char) word[i]);

            //Check if there are vowels (lowercase or not)
            if (tempLetter == 'a' || tempLetter == 'e' || tempLetter == 'i' || tempLetter == 'o' || tempLetter == 'u') {
                
                foundVowels++;

                //Check if the vowel was found or not before by a previous call of the function from another process
                //And the index of the process tells us (maxNumVowels) how many vowels must be found before we make changes to the word 
                if (foundVowels == maxNumVowels){
                    //If it was found, we just copy the word as it is
                    newWord[v++] = 'p';
                    newWord[v++] = word[i];
                    newWord[v++] = 'p';
                    continue;
                }   
            }
            newWord[v++] = word[i];    
        }
        strcpy(word, newWord);
    }
    
    free(newWord);
}

//When last child process is created, the first process will get the word from the user
void handleLastProcessCreated(int sig){

    printf("\nThe starting word is: ");
    scanf("%s", word);

}

void handleParentProcessResume(int sig){

    //Will be put to sleep for 10ms
    usleep(10000);
}

int main(){

    //Creating the FIFO file for inter-process communication:

    if (mkfifo(FIFOFILE, 0666) == -1){
        printf("File probably exists already\n");
        
    }

    //The total number of players is PLAYERS = total number of processes (n child processes + 1 parent process) 

    // Number of child processes to be created
    int n = PLAYERS -1;
   

    word = (char*)malloc(WORDLENGTH*sizeof(char));
    

    int i, childID;
    
    /*
    We create n child processes sequentially (0 -> 1 -> 2 -> 3 -> 4 -> ... -> n) break them out of the loop and pause them, once we've created the nth child process, we signal the parent process (0)
    to start the game, it will read the word from the terminal, then pass it to its child process and 
    each child process will distort the word and pass it on to the next one through a FIFO file until we reach the last process
    then we print the final result
    */

    int firstPersonProcessID = getpid();

    for (i = 0; i < n; i++){


        childID = fork();

        if (childID == -1){
            printf("Error creating child process\n");
            return 1;
        }

        //Check if the process is a child or parent process:
        
        if (childID == 0){

            //Check if it's the last child process
            if (i == n-1){

                kill(firstPersonProcessID, SIGUSR1);
            }
        }else{
            break;
        }
        
    }

    if (i != 0){//Child Processes

        //Pause the current process until it gets resumed by the parent process
        struct sigaction parentProcessResume;
        parentProcessResume.sa_handler = &handleParentProcessResume;
        sigaction(SIGUSR2, &parentProcessResume, NULL);
        pause();

        //Open FIFO file for reading:
        int fd;

        if ((fd = open(FIFOFILE, O_RDONLY)) == -1){
            printf("Error opening FIFO file\n");
            return 1;
        }

        //Read the word from the FIFO file
        if (read(fd, word, WORDLENGTH*sizeof(char)) == -1){
            printf("Error reading from FIFO file\n");
            return 2;
        }

        close(fd);

    }else{//First (Parent) Process

        //Wait for the last child process to be created and signal the first process
        struct sigaction lastProcessCreated;
        lastProcessCreated.sa_handler = &handleLastProcessCreated;
        sigaction(SIGUSR1, &lastProcessCreated, NULL);
        pause(); 
    }

    //If this is the last process, we will print the final result and delete the fifo file
    if (i == n){
        
        printf("\nFinal word: %s\n", word);

        //Delete the FIFO file after we're done with it:
        if (unlink(FIFOFILE) == -1){
            printf("Error deleting FIFO file\n");
        }
        free(word);
        return 0;
    }

    //Signal the child process to resume execution so it can read the word from the FIFO file
    kill(childID, SIGUSR2);

    //Opening the FIFO file for writing
    int fd; 
    fd = open(FIFOFILE, O_WRONLY);

    if (fd == -1){
        printf("Error opening FIFO file\n");
        return 1;
    }
    
    distortWord(i+1);
    
    //Write to the FIFO file the new word
    if (write(fd, word, strlen(word)) == -1){

        printf("Error writing to FIFO file\n");
        return 2;
    }
    printf("Person %d: said the word: %s\n", i+1,word);

        
    //Close the FIFO file
    close(fd);       

    //Wait for all child processes to finish execution
    while(wait(NULL)>0);

    free(word);
    return 0;
}