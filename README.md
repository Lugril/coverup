# CoverUp: LLM-Powered Python Test Coverage Improver
by [Juan Altmayer Pizzorno](https://jaltmayerpizzorno.github.io) and [Emery Berger](https://emeryberger.com)
at UMass Amherst's [PLASMA lab](https://plasma-umass.org/).

[![pypi](https://img.shields.io/pypi/v/coverup?color=blue)](https://pypi.org/project/coverup/)
![pyversions](https://img.shields.io/pypi/pyversions/coverup)

## About CoverUp
CoverUp adds to your module's test suite so that more of its code gets tested
(i.e., increases its [code coverage](https://en.wikipedia.org/wiki/Code_coverage)).
It can also create a suite from scratch if you don't yet have one.
The new tests are based on your code, making them useful for [regression testing](https://en.wikipedia.org/wiki/Regression_testing).

CoverUp is designed to work closely with the [pytest](https://docs.pytest.org/en/latest/) test framework.
To generate tests, it first measures your suite's coverage using [SlipCover](https://github.com/plasma-umass/slipcover)
and selects portions of the code that need more testing.
It then engages in a conversation with an [LLM](https://en.wikipedia.org/wiki/Large_language_model),
prompting for tests, checking the results and re-prompting for adjustments as necessary.
Finally, CoverUp checks that the new tests integrate well, attempting to resolve any issues it finds.

## Installing
CoverUp is available from PyPI, so you can install simply with
```shell
python3 -m pip install coverup
```

While we intend to also support local LLMs, currently CoverUp requires an [OpenAI account](https://platform.openai.com/signup) to run.
Your account will also need to have a [positive balance](https://platform.openai.com/account/usage).
Create an [API key](https://platform.openai.com/api-keys) and store its "secret key" (usually a
string starting with `sk-`) in an environment variable named `OPENAI_API_KEY`:
```shell
export OPENAI_API_KEY=<...your-api-key...>
```

## Using
If your module's source code is in `src` and your tests in `tests`, you can run CoverUp as
```shell
coverup --source-dir src --tests-dir tests
```
CoverUp then creates tests named `test_coverup_N.py`, where `N` is a number, under the `tests` directory.

### Example
Here we have CoverUp create additional tests for the popular package [Flask](https://flask.palletsprojects.com/):
```
$ coverup --source-dir src/flask --tests-dir tests
Measuring test suite coverage...  starting coverage: 90.2%
Prompting gpt-4-1106-preview for tests to increase coverage...
100%|███████████████████████████████████████████████████| 95/95 [02:49<00:00,  1.79s/it, usage=~$3.30, G=51, F=141, U=22, R=0]
Checking test suite...  tests/test_coverup_2.py is failing, looking for culprit(s)...
Disabling tests/test_coverup_19.py
Checking test suite...  tests ok!
Measuring test suite coverage...  end coverage: 94.2%
```
In just short of 3 minutes, CoverUp increased Flask's test coverage from 90.2% to 94.2%.
It then detected that one of the new tests, `test_coverup_19`, was causing another test
to fail and disabled it.
That test remains as `disabled_test_coverup_19.py`, where it can be reviewed for the cause
and possibly re-added to the suite.

### Better With Docker
To evaluate the tests generated by the LLM, CoverUp must execute them.
For best security and to minimize the risk of damage to your system, we recommend
running CoverUp with [Docker](https://www.docker.com/).

## Evaluation
<img src="images/comparison.png?raw=True" align="right" width="65%"/>

The graph shows CoverUp in comparison to the state-of-the-art [CodaMosa](https://www.carolemieux.com/codamosa_icse23.pdf),
which improves upon the [Pynguin](https://github.com/se2p/pynguin) test generator by incorporating LLM queries.
The bars show the difference in coverage percentage between CoverUp and CodaMosa for various Python modules;
green bars, above 0, indicate that CoverUp achieved a higher coverage.

As the graph shows, CoverUp achieves better coverage in almost every case.
Both CoverUp and CodaMosa created tests "from scratch", that is, ignoring any existing test suite.

<br/>

## Work In Progress
This is an early release of CoverUp.
Please enjoy it, and pardon any disruptions as we work to improve it.

## Acknowledgements
This material is based upon work supported by the National Science
Foundation under Grant No. 1955610. Any opinions, findings, and
conclusions or recommendations expressed in this material are those of
the author(s) and do not necessarily reflect the views of the National
Science Foundation.
