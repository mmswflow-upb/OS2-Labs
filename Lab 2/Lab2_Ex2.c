#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <dirent.h>


#define WORD_LENGTH 300
#define PATH "TextFiles"
#define PATH_LENGTH 200
int wordCount;
char* word;



//Counts the number of occurances of a word in a given file
void* wordCounter(void* arg){


    char* filePath = (char*)arg;
    char tempWord[WORD_LENGTH];

    printf("File: %s\n", filePath);

    FILE* file = fopen(filePath, "r");



    if (file == NULL){
        printf("Error! Unable to open file.\n");
        return NULL;
    }
    
    
    while (fscanf(file, " %s ", tempWord) != EOF){
        printf("Word: %s\n", tempWord);
        if (strcmp(tempWord, word) == 0){
            wordCount++;

        }
    }

    fclose(file);
}

//Lists all the files in the directory recursively
void listFiles(const char* dirName){

     //Opening the directory in order to loop through the files
    DIR* dir = opendir(dirName);

    if (dir == NULL){

        printf("Error! Unable to open directory.\n");
        return;
    }


    struct dirent* entity;
    entity = readdir(dir);

    //Start a thread for each file in the directory
    while (entity != NULL){


        if (strcmp(entity->d_name, ".") == 0 || strcmp(entity->d_name, "..") == 0){
            entity = readdir(dir);
            continue;
        }


        char* fileName = entity->d_name;


        //Create the file path
        char filePath[100] = {0};
        strcat(filePath, dirName);
        strcat(filePath, "/");
        strcat(filePath, fileName);


        entity = readdir(dir);
            
        //Create a thread for each file
        pthread_t threadID;
        pthread_create(&threadID, NULL, wordCounter, (void *)&filePath);
        pthread_join(threadID, NULL);
    }
    
    closedir(dir);
}

int main(){

    //Intialize the word count to 0
    wordCount = 0;

    //Allocate memory for the word
    word = (char*)malloc(WORD_LENGTH*sizeof(char));

    printf("\nInput a word to search for: ");
    scanf("%s", word);

    listFiles(PATH);

    //Wait for all threads to finish
    printf("The total word count is: %d\n", wordCount);

    return 0;
}