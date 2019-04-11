# walking_marvin
Train a 2-legged robot to walk in [Gym](https://gym.openai.com/) environment by implementing [Evolution Strategies](https://openai.com/blog/evolution-strategies/) in Python. (42 Silicon Valley)

![walking](https://github.com/ashih42/walking_marvin/blob/master/Screenshots/walking.gif)

`Marvin` environment was adapted from [BipedalWalker-v2](https://github.com/openai/gym/wiki/BipedalWalker-v2) and has the same input/output space:
* Input Observation: 24 values
* Output Action: 4 values

## Prerequisites

You are on macOS with `python3` installed.

## Installing

```
./setup/setup.sh
```

## Running

### Training
```
python3 marvin.py -t [-l old_file] [-m t_max] [-e n_episodes] [-s new_file]
```
* `-t` Train.
* `-l old_file` Load save from `old_file`.
* `-m t_max` Set `t_max` for training (200 by default)
* `-e n_episodes` Train for `n_espidoes` (10 by default).
* `-s new_file` Save afterwards in `new_file`.

### Walking
```
python3 marvin.py -w [-e n_episodes] [-l old_file]
```
* `-w` Walk.
* `-l old_file` Load save from `old_file`.
* `-e n_episodes` Walk for `n_episodes` (10 by default).

### Other Options
* `-z seed` Set `seed` value for environment.
* `-b` Run [BipedalWalker-v2](https://gym.openai.com/envs/BipedalWalker-v2/) instead.
* `-bh` Run [BipedalWalkerHardcore-v2](https://gym.openai.com/envs/BipedalWalkerHardcore-v2/) instead.
* `-q` Play [QWOP](http://www.foddy.net/Athletics.html).
  * `Left Alt`, `Left Command`, `Right Control`, `Right Shift`.
* `-qx` Play QWOP EXTREME.
