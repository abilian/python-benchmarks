const ITERATIONS = 100;
const EXPECTED = 8939;

function mandelbrot() {
  let count = 0;

  let h = 150.0;
  let y = 0.0;
  let Z = 0.0;
  let z = 0.0;
  let T = 0.0;
  let t = 0.0;
  let C = 0.0;
  let c = 0.0;
  let U = 0.0;
  let V = 0.0;
  let K = 1.5;
  let k = 1.0;

  while (y < 150) {
    y += 1;
    let x = 0.0;
    while (x < 150) {
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

      let i = 0;
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


for (let i = 0; i < ITERATIONS; i++) {
  const result = mandelbrot();
  if (result != EXPECTED) {
    throw "Error: got " + result + " expected " + EXPECTED;
  }
}
