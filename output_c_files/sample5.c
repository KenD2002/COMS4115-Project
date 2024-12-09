#include <stdio.h>
#include <string.h>

int main() {
    int x = 0;
    while ((x > 5)) {
        printf("%s\n", "x is: ");
        printf("%d\n", x);
        x = (x + 1);
    }
    while ((x < 5)) {
        printf("%s\n", "x is: ");
        printf("%d\n", x);
        int y = -2;
        while ((y < 0)) {
            printf("%s\n", "y is : ");
            printf("%d\n", y);
            y = (y + 1);
        }
        x = (x + 1);
    }
    return 0;
}
