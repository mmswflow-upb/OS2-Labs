#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>

#define WORDLENGTH 300
#define PLAYERS 5
#define FIFOFILE "ex1Fifo"


//Distorts given word based on 2 algorithms and returns the new word
char* distortWord(char* word){

    int length = strlen(word);
    char* newWord = (char*)malloc(length * sizeof(char));

    //Seeding the random number generator based on the current time and the process ID
    srand(time(NULL) ^ getpid());

    //Generating a random number (0 or 1) to decide which distortion algorithm to use
    int random = rand() % 2;

    //( 0 is for Reversing the word, 1 is for switching D with T and T with D, 2 is for no distortion)
    if (random == 0){
    
        for (int i = 0; i < length; i++) {
            newWord[i] = word[length - i - 1];
        }

    }else if (random == 1){

        for (int i = 0; i < length; i++) {
            if (word[i] == 'd'){
                newWord[i] = 't';
            }else if (word[i] == 't'){
                newWord[i] = 'd';
            }else if(word[i] == 'D'){
                newWord[i] = 'T';
            }else if(word[i] == 'T'){
                newWord[i] = 'D';

            }else{
                newWord[i] = word[i];
            }
        }
    }else{
        newWord = word;
    }

    free(word);
    return newWord;

}


int main() {

    //Creating the FIFO file for inter-process communication:

    if (mkfifo(FIFOFILE, 0666) == -1){
        printf("File probably exists already\n");
        
    }

    //The total number of players is PLAYERS = total number of processes (n child processes + 1 parent process) 

    // Number of child processes to be created
    int n = PLAYERS -1;


    //Game Results in (-1)^n * word (-1 meaning the word is reversed, 1 meaning the word is not reversed)
    //^^ It could also include some distortions from the second algorithm, but generally it will be clear which alg. was applied

    char* word = (char*)malloc(WORDLENGTH*sizeof(char));
    
    //Get the word from the user
    printf("Person 1 said: ");
    scanf("%s", word);

    int i, childID;
    

    /*
    Creates n child processes sequentially (1 -> 2 -> 3 -> 4 -> 5 -> .... -> n)

    1-> 1 & 2 -> 1 breaks loop, 2 continues
    2-> 2 & 3 -> 2 breaks loop, 3 continues
    3-> 3 & 4 -> 3 breaks loop, 4 continues
    4-> 4 & 5 -> 4 breaks loop, 5 continues but reaches end of loop
    and so on
    */
    for (i=0; i < n; i++){

        //Fork the process into two processes
        childID = fork();
        

        //Checks if the process is a child process
        if (childID == 0){
           
            //This is the child process born from the fork above, it will open the fifo file to read the distorted word and print it
        
            word = (char*)malloc(WORDLENGTH*sizeof(char));

            int fd;
            fd = open(FIFOFILE, O_RDONLY);
            if (fd == -1){
                printf("\nAt Process: %d | Error opening file\n", i+2);
                return 1;
            }

            if (read(fd, word, 300*sizeof(char)) == -1){
                printf("\nAt Process: %d | Error reading from file\n", i+2);
                return 2;
            }

            close(fd);
            printf("\nPerson %d heard the word: %s\n", i+2, word);
            
            //Sleep for 50 ms:
            usleep( 100* 1000 );
        
        }else{

            //This is the parent process, it will open the fifo file to write the distorted word and pass it 
            //on to the child process which mush read it
            
            
            
            word = distortWord(word);

            int fd;
            fd = open(FIFOFILE, O_WRONLY);
            
            if (fd == -1){
                printf("\nAt Process: %d | Error opening file\n", i+1);
                return 1;
            }

            if (write(fd, word, strlen(word)) == -1){
                printf("\nAt Process: %d | Error writing to file\n", i+1);
                return 2;
            }

            close(fd);
            break;

        }
    }

    //Wait for all child processes to finish execution
    while(wait(NULL)>0);

    if (i == n){
        printf("\nFinal word: %s\n", word);
        
        //Delete the FIFO file after we're done with it:
        if (unlink(FIFOFILE) == -1){
            printf("Error deleting FIFO file\n");
        }

    }

    //Free the memory allocated for the word
    free(word);

    return 0;
}