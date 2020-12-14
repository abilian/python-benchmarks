import os, time


def measure(func, repetitions, size):
    t0 = time.time()
    func(repetitions, size)
    print(
        func,
        "%d bytes, %.2fus per write"
        % (size, (time.time() - t0) / repetitions * 1000 * 1000),
    )


def fwrite(repetitions, size):
    fd = os.open("/dev/null", os.O_WRONLY)
    for i in range(repetitions):
        os.write(fd, b" " * size)


def fread(repetitions, size):
    fd = os.open("/dev/zero", os.O_RDONLY)
    for i in range(repetitions):
        os.read(fd, size)


def file_write(repetitions, size):
    f = open("/dev/null", "w")
    for i in range(repetitions):
        f.write(" " * size)
    f.flush()


def file_read(repetitions, size):
    f = open("/dev/zero")
    for i in range(repetitions):
        f.read(size)


if __name__ == "__main__":
    measure(fread, 1000000, 100)
    measure(fwrite, 1000000, 100)
    measure(fread, 1000000, 1000)
    measure(fwrite, 1000000, 1000)
    measure(fread, 100000, 10000)
    measure(fwrite, 100000, 10000)
    measure(file_read, 1000000, 100)
    measure(file_write, 1000000, 100)
    measure(file_read, 1000000, 1000)
    measure(file_write, 1000000, 1000)
    measure(file_read, 100000, 10000)
    measure(file_write, 100000, 10000)
