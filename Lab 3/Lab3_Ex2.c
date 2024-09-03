
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

#define PARKING_SPACES 1
#define NUM_CARS 5

/*
HOW IT WORKS:

    Car threads will call the parkCar function
    They are added to a queue, in the order they arrive
    They will wait for a free parking space
    When a parking space is free, they will be removed from the queue and parked
    After 2 seconds, they will leave the parking space
    The parking space will be free again
*/

// Global variables
sem_t freeParkingSpaces;
pthread_mutex_t carQueueLock;
int carQueue[NUM_CARS];
int queueIndex = 0;

// Push a car into the queue
void pushQueue(int carId)
{

    carQueue[queueIndex] = carId;
    queueIndex++;
}

// Pop a car from the queue
int popQueue()
{

    int carId = carQueue[0];
    int i;
    // Shift all elements to the left after popping the first element
    for (i = 0; i < queueIndex - 1; i++)
    {
        carQueue[i] = carQueue[i + 1];
    }
    queueIndex--;
    return carId;
}

// Car Thread function
void *parkCar(void *arg)
{

    // Car Identifier
    int carId = *(int *)arg;

    // Critical Section, we're adding a car to the queue
    pthread_mutex_lock(&carQueueLock);
    pushQueue(carId);
    printf("CAR %d ARRIVED\n", carId);
    pthread_mutex_unlock(&carQueueLock);

    // Wait for a free parking space
    sem_wait(&freeParkingSpaces);

    // Critical Section, we're removing a car from the queue
    pthread_mutex_lock(&carQueueLock);
    carId = popQueue();
    pthread_mutex_unlock(&carQueueLock);

    printf("\nCar %d parked\n", carId);
    sleep(2);

    // Signal that a parking space is free
    sem_post(&freeParkingSpaces);

    printf("Car %d left\n", carId);

    // Free the memory allocated for the car identifier
    free(arg);
    return NULL;
}

int main()
{

    pthread_t cars[NUM_CARS];

    // Initializing the semphore and the mutex
    sem_init(&freeParkingSpaces, 0, PARKING_SPACES);
    pthread_mutex_init(&carQueueLock, NULL);

    int i;

    // Create the car threads
    for (i = 0; i < NUM_CARS; i++)
    {
        // Creating a copy of the car identifier to pass it to the thread (through dynamic allocation)
        int *i_copy = malloc(sizeof(int));
        *i_copy = i + 1;
        if (pthread_create(&cars[i], NULL, parkCar, (void *)i_copy) != 0)
        {
            printf("Error creating thread\n");
            exit(1);
        }
    }

    // Wait for all car threads to finish execution
    for (i = 0; i < NUM_CARS; i++)
    {
        pthread_join(cars[i], NULL);
    }

    // Destroy the semaphore and the mutex
    sem_destroy(&freeParkingSpaces);
    pthread_mutex_destroy(&carQueueLock);

    return 0;
}
