#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define YEARS 10
#define INTIALSUM 100

//Global variable which holds the sum
double sum;

//Add Interest to the sum yearly (0.7% * 12)
void* addInterest(void *vargp)
{

    //wait 1 second
    sleep(1);

    //Add the interest
    sum = sum*1.084;
    
    printf("Year %d: $%.6f\n", *(int*)vargp, sum);

    return NULL;
}

int main(){

    

    pthread_t tid;
    
    sum = INTIALSUM;

    for (int i = 0; i < YEARS; i++){

        pthread_join(tid, NULL);
        int year = i+1;
        pthread_create(&tid, NULL, addInterest, (void*)&year);

    }
    //Wait for all threads to finish
    pthread_exit(NULL);

    return 0;
}
