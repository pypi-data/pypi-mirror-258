# PyOMP

This is a fork of the abandoned OMPEval project, an extremely fast Texas Hold'em hand evaluator written by zekyll in
C++, now wrapped in Python.

## Installation

```pip install pyomp```
*Note: I've only built this for Python 3.11 for now.*

# Development Environment

1. Build the needed libraries using cmake.
2. Build the python wrapper using setup.py
```shell
python setup.py build_ext --inplace
```
# Example
```python
from pyomp import EquityCalculator

ec = EquityCalculator()
ec.run(['2c8h', '2s8d', '66+', 'ako', '7ko+', 'aa'], 'jctcad')

for i, equity in enumerate(ec.equity):
    print(f'Player {i}: {equity:.2%}')
```