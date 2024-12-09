#include <stdio.h>
#include <string.h>

int haha(int x, int y) {
    x = (x + 1);
    y = (y + x);
    return y;
}

int main() {
    int x = 10;
    int n = (haha(x, 5) + 10);
    printf("%d\n", n);
    return 0;
}
