#include <stdlib.h>
#include <stdio.h>
#include "utils.h"

#define N 10

int main(void)
{
    int i, v[N] = {10, -20, 30, 9, 7, 8, 11, 5, -2, -100};

    printf("Values: ");
    for (i = 0; i < N; ++i)
    {
        printf("%d ", v[i]);
    }
    printf("\n");

    printf("Values greater than %d: %d\n", MIN_VAL, vect_gt(v, N, MIN_VAL));
    printf("Values less than %d: %d\n", MAX_VAL, vect_lt(v, N, MAX_VAL));

    return 0;
}