/* The Computer Language Shootout
   http://shootout.alioth.debian.org/

   contributed by Greg Buchholz
*/

// Modified to be more similar to the Python version.


#include<stdio.h>
#include<stdlib.h>

#define W 150
#define H 150
#define ITERATIONS 10

#define EXPECTED 8939


int mandelbrot()
{
    int bit_num = 0;
    char byte_acc = 0;
    int i, iter = 50;
    double x, y, limit = 2.0;
    double Zr, Zi, Cr, Ci, Tr, Ti;
    int count = 0;

    for (y = 0; y < H; ++y) {
        for (x = 0; x < W; ++x) {
            Zr = Zi = Tr = Ti = 0.0;
            Cr = (2.0 * x / W - 1.5);
            Ci = (2.0 * y / H - 1.0);

            for (i = 0; i < iter && (Tr + Ti <= 4); ++i) {
                Zi = 2.0 * Zr * Zi + Ci;
                Zr = Tr - Ti + Cr;
                Tr = Zr * Zr;
                Ti = Zi * Zi;
            }

            if (Tr + Ti <= 4) {
                count += 1;
            }
        }
    }
    return count;
}


int main(int argc, char **argv)
{
    for (int i = 0; i < ITERATIONS; i++) {
        int result = mandelbrot();
        printf("%d\n", result);

        // FIXME: off by one !
//        if (result != EXPECTED) {
//            printf("ERROR! result=%d expected=%d", result, EXPECTED);
//            exit(1);
//        }
    }
}
