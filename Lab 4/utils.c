#include <stdlib.h>
#include "utils.h"

int vect_gt(int *v, int n, int val)
{
    if (n < 0)
        return 0;
    return v[n] > val ? 1 + vect_gt(v, n - 1, val) : vect_gt(v, n - 1, val);
}

int vect_lt(int *v, int n, int val)
{
    if (n < 0)
        return 0;
    return v[n] < val ? 1 + vect_lt(v, n - 1, val) : vect_lt(v, n - 1, val);
}