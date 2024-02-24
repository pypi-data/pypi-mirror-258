# TinyRL
A Python wrapper for RLtools ([https://rl.tools](https://rl.tools)). PyTorch is only used for its [utils that allow convenient wrapping of C++ code](https://pytorch.org/docs/stable/cpp_extension.html) to compile RLtools. The RLtools training code needs to be compiled at runtime because properties like the observation and action dimensions are not known at compile time. One of the fundamental principles of RLtools is that the sizes of all data structures and loops are known at compile-time so that the compiler can maximally reason about the code and heavily optimize it. Hence this wrapper takes an environment ([Gymnasium](https://github.com/Farama-Foundation/Gymnasium) interface) factory function as an input to infer the observation and action shapes and compile a bridge environment that is compatible with RLtools. 

This wrapper is work in progress and for now just exposes the SAC training loop and does not allow much modification of hyperparameters etc. yet. Stay tuned.

### Installation:
```
pip install tinyrl
```
For the following example:
```
pip install gymnasium
```

### Example:
```
from tinyrl import loop_sac
import gymnasium as gym

def env_factory():
    return gym.make("Pendulum-v1")

loop = loop_sac(env_factory)

loop_state = loop.LoopState()
loop.init(loop_state, 0)

finished = False
step = 0
while not finished:
    if(step % 100 == 0):
        print(f"Step {step}")
    finished = loop.step(loop_state)
    step += 1
```

