EXPECTED = 8939

function mandelbrot()
    count = 0

    h = 150
    Z = 0.0
    z = 0.0
    T = 0.0
    t = 0.0
    C = 0.0
    c = 0.0
    U = 0.0
    V = 0.0
    K = 1.5
    k = 1.0

    y = 0
    while y < 150 do
        y = y + 1
        x = 0
        while x < 150 do
            x = x + 1
            Z = 0.0
            z = 0.0
            T = 0.0
            t = 0.0
            U = x * 2
            U = U / h
            V = y * 2
            V = V / h
            C = U - K
            c = V - k

            i = 0
            while i < 50 do
                i = i + 1
                if T + t <= 4 then
                    z = Z * z
                    z = z * 2
                    z = z + c
                    Z = T - t
                    Z = Z + C
                    T = Z * Z
                    t = z * z
                end
            end

            if T + t <= 4 then
                count = count + 1
            end
        end
    end

    return count
end

for i = 1, 10 do
    result = mandelbrot()
    if (result ~= EXPECTED) then
        error(string.format("Expected %d got %d", EXPECTED, result))
    end
end
