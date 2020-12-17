import os, time

from numba import jit


@jit
def fwrite(repetitions, size):
    data = b" " * size
    fd = os.open("/dev/null", os.O_WRONLY)
    for i in range(repetitions):
        os.write(fd, data)


@jit
def fread(repetitions, size):
    fd = os.open("/dev/zero", os.O_RDONLY)
    for i in range(repetitions):
        os.read(fd, size)


if __name__ == "__main__":
    fread(1000000, 100)
    fwrite(1000000, 100)
    fread(1000000, 1000)
    fwrite(1000000, 1000)
    fread(100000, 10000)
    fwrite(100000, 10000)
