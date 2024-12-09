#include <stdio.h>
#include <string.h>

int main() {
    double pi = 3.14;
    char* greetings[] = {"hello", "world"};
    char* msg = "";
    msg = greetings[0];
    printf("%s\n", msg);
    double val = (pi * 2.0);
    printf("%f\n", val);
    return 0;
}
