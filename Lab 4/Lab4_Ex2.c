
#include <stdio.h>
#include <pthread.h>
#include <string.h>
#include <stdlib.h>

// Public key:
int n, e, phi, msg_len;

// Greatest common divisor
int gcd(int a, int b)
{
    if (b == 0)
    {
        return a;
    }
    return gcd(b, a % b);
}

// Computes x^y mod p
int power_mod(int m, unsigned int e, int n)
{
    int res = 1;
    m = m % n;
    while (e > 0)
    {
        if (e & 1)
        {
            res = (res * m) % n;
        }
        e = e >> 1;
        m = (m * m) % n;
    }
    return res;
}

void *receiver(void *arg)
{

    int *encrypted_msg = (int *)arg;

    // Finding d

    int d = 2;

    while (d * e % phi != 1)
    {
        d++;
    }

    char decrypted_msg[msg_len + 1];

    for (int i = 0; i < msg_len; i++)
    {
        decrypted_msg[i] = power_mod(encrypted_msg[i], d, n);
    }
    decrypted_msg[msg_len] = '\0';

    printf("\nDecrypted message: %s\n", decrypted_msg);
}

void *sender(void *arg)
{

    char *msg = (char *)arg;
    msg_len = strlen(msg);

    // Prime numbers used for encryption
    int p = 83;
    int q = 11;

    phi = (p - 1) * (q - 1);

    // Public key
    n = p * q;
    e = 65537;

    int encrypted_msg[strlen(msg) + 1];

    printf("\nEncrypted message:");
    for (int i = 0; i < msg_len; i++)
    {
        encrypted_msg[i] = power_mod(msg[i], e, n);
        printf("%d ", encrypted_msg[i]);
    }
    encrypted_msg[msg_len] = '\0';

    // Send encrypted message to receiver thread
    pthread_t receiver_thread;
    pthread_create(&receiver_thread, NULL, receiver, (void *)encrypted_msg);

    // Wait for receiver thread to finish
    pthread_join(receiver_thread, NULL);
}

int main()
{

    pthread_t sender_thread;

    char *msg = "Hello World";
    printf("\nOriginal message: %s\n", msg);
    char msgArr[strlen(msg) + 1];
    strcpy(msgArr, msg);
    msgArr[strlen(msg)] = '\0';

    pthread_create(&sender_thread, NULL, sender, (void *)msg);

    // Wait for sender thread to finish
    pthread_join(sender_thread, NULL);
    return 0;
}
