# PyOMP

This is a fork of the abandoned OMPEval project, an extremely fast Texas Hold'em hand evaluator written by zekyll in
C++, now wrapped in Python.

# Quick start

I'm in the very early stages but the package can be built and run using

```shell
python setup.py build_ext --inplace
```

```python
import OMPEval

print('start')
eq = OMPEval.PyEquityCalculator()
eq.set_time_limit(.1)
eq.start(['2c8h', '2s8d'],
	 board_cards='jctc1d',
	 dead_cards=None,
	 enumerate_all=False,
	 stdev_target=5e-5,
	 update_interval=0.2,
	 thread_count=0
	 )
eq.wait()
results = eq.get_results()
for key, value in results.items():
	print(key, value)

print('finished')
```