## Difference between modules
How long does it take to log 1000 debug messages to the console?

| Module                     | Avg. Time out of 3 tries |
|----------------------------|--------------------------|
| logging                    | 0.986                    |
| colorlog                   | 1.286                    |
| neatlog v0.0.3             | 8.602   holy crap!!!     |
| neatlog v0.0.3 (no colors) | 8.245   holy crap!!!     |
| neatlog v2.0.0             | 1.334   that's better    |
| neatlog v2.0.0 (no colors) | 0.967   mmmmh            |
