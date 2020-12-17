import os


cdef fwrite(int num, int num2):
    fd = os.open("/dev/null", os.O_WRONLY)
    data = b" " * num2
    for i in range(num):
        os.write(fd, data)


cdef fread(int num, int num2):
    fd = os.open("/dev/full", os.O_RDONLY)
    for i in range(num):
        os.read(fd, num2)


if __name__ == '__main__':
    fread(1000000, 100)
    fwrite(1000000, 100)
    fread(1000000, 1000)
    fwrite(1000000, 1000)
    fread(100000, 10000)
    fwrite(100000, 10000)
