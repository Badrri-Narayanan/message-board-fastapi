#include<stdio.h>

int factorial(int n) {
    if(n<2)
        return n;
    return n * factorial(n-1);
}

int main() {
    return 0;
}