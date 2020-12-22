/* Translated to Java from the JavaScript version.
*/

class mandelbrot {
    private final static int SIZE = 150;
    private final static int ITERATIONS = 100;
    private final static int EXPECTED = 8939;

    public static void main(String[] args) throws Exception {
        for (int i = 0; i < ITERATIONS; i++) {
            int result = mandelbrot();

            if (result != EXPECTED) {
                String msg = String.format("Computation result incorrect, was %d", result);
                throw new AssertionError(msg);
            }
        }
    }

    public static int mandelbrot() {
        int count = 0;

        int h = SIZE;
        double Z = 0.0;
        double z = 0.0;
        double T = 0.0;
        double t = 0.0;
        double C = 0.0;
        double c = 0.0;
        double U = 0.0;
        double V = 0.0;
        double K = 1.5;
        double k = 1.0;

        double y = 0.0;
        while (y < SIZE) {
            y += 1;

            double x = 0.0;
            while (x < SIZE) {
                x += 1;
                Z = 0.0;
                z = 0.0;
                T = 0.0;
                t = 0.0;
                U = x * 2;
                U /= h;
                V = y * 2;
                V /= h;
                C = U - K;
                c = V - k;

                int i = 0;
                while (i < 50) {
                    i += 1;
                    if (T + t <= 4) {
                        z = Z * z;
                        z *= 2;
                        z += c;
                        Z = T - t;
                        Z += C;
                        T = Z * Z;
                        t = z * z;
                    }
                }
                if (T + t <= 4) {
                    count += 1;
                }
            }
        }
        return count;
    }
}
