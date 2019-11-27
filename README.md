# quantum-fun

## Current Problems:

Utilizing 15 as the number to factor, the random guess of x = 2 returns a period of either 1 or 4 with fairly consistent precision (running each circuit with 1000 shots, and running each x 20 times)
When x = 11, about half of the runs output the wrong factors
When x = 14, error handling needs to be improved (it should return 1 and 15 as the factors which are not helpful, but currently that is only happening 25% of the time)
