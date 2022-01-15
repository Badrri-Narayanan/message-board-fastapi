#include<stdio.h>

long factorial(int a) {
    long fact = 1;
    if(a < 1) {
        return fact;
    }
    return a * factorial(a-1);
}
