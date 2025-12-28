# AxLang vs Python Benchmark Results

Generated: 2025-12-28 17:47:46

## Summary

| Benchmark | AxLang (s) | Python (s) | Ratio (AxLang/Python) |
|-----------|------------|------------|----------------------|
| Fibonacci (n=25) | 5.9810 | 0.0366 | 163.25x |
| Factorial (n=1000) | 0.1692 | 0.0285 | 5.94x |
| Prime Numbers (limit=1000) | 0.0000 | 0.0275 | 0.00x |
| Nested Loops (n=100) | 0.3948 | 0.0289 | 13.65x |
| Function Calls (n=10000) | 0.4005 | 0.0294 | 13.63x |
| List Operations (n=1000) | 0.0000 | 0.0280 | 0.00x |
| Recursion - Ackermann(3,6) | 0.0000 | 0.0386 | 0.00x |

## Detailed Results

### Fibonacci (n=25)

- **AxLang**: 5.9810s
- **Python**: 0.0366s
- **Ratio**: 163.25x (AxLang is 163.25x slower)

### Factorial (n=1000)

- **AxLang**: 0.1692s
- **Python**: 0.0285s
- **Ratio**: 5.94x (AxLang is 5.94x slower)

### Prime Numbers (limit=1000)

- **AxLang**: 0.0000s
- **Python**: 0.0275s
- **Ratio**: 0.00x 