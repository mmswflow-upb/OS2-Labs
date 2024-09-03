
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define NUM_ORDERS 10

pthread_mutex_t cookLock;

// Order thread function, takes order number as argument and cooks the orders one at a time using a lock
void *cookOrder(void *arg)
{

    pthread_mutex_lock(&cookLock);
    printf("\nReceived order %d...\n", *(int *)arg);
    sleep(2);
    printf("Order %d cooked\n", *(int *)arg);
    pthread_mutex_unlock(&cookLock);

    // Freeing the memory of the copy of the order number
    free(arg);
    return NULL;
}

int main()
{

    int i;
    pthread_t orders[NUM_ORDERS];

    pthread_mutex_init(&cookLock, NULL);

    // Creating order threads and passing order number as argument
    for (i = 0; i < NUM_ORDERS; i++)
    {

        int *i_copy = malloc(sizeof(int));
        *i_copy = i + 1;
        if (pthread_create(&orders[i], NULL, cookOrder, (void *)i_copy) != 0)
        {
            printf("Error creating thread\n");
            exit(1);
        }
    }

    // Waiting for all order threads to finish
    for (i = 0; i < NUM_ORDERS; i++)
    {
        pthread_join(orders[i], NULL);
    }

    // Destroying the lock
    pthread_mutex_destroy(&cookLock);
    return 0;
}
