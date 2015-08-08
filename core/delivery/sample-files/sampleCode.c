/* @file sample.c
 * @brief Sample C file.
 * @since 8 August 2015
 * @author Oscar Bezi, bezi@scottylabs.org
 */

#include <stdio.h>

unsigned int fib(unsigned int n) {
    switch (n) {
        case 0:
        case 1:
            return 1;
        default:
            return fib(n - 1) + fib(n - 2);
    }
}

int main() {
    printf("Hello, world!\n");
    printf("%u\n", fib(3));
}
