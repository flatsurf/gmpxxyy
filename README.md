![Test](https://github.com/flatsurf/gmpxxyy/workflows/Test/badge.svg)

# Python Wrapper for GMP

This is another Python wrapper for [GMP](https://gmplib.org/).

This wrapper is powered by [cppyy](https://cppyy.readthedocs.io/), i.e., it wraps `libgmpxx`, the [C++ interface of GMP](https://gmplib.org/manual/C_002b_002b-Class-Interface.html#C_002b_002b-Class-Interface).

## Comparison to Existing Wrappers

There might be others out there but we are aware of these Python wrappers for GMP.

* [gmpy](https://pypi.org/project/gmpy/) and [gmpy2](https://github.com/aleaxit/gmpy)

This wrapper was born out of the necessity for a wrapper for the C++ interface of GMP for [pyexactreal](https://github.com/flatsurf/exact-real) so the semantics are exactly the same as in the [C++ interface](https://gmplib.org/manual/C_002b_002b-Class-Interface.html#C_002b_002b-Class-Interface) and the Python code involved is quite minimal. It does not actually aim to compete with any of the existing wrappers, we just needed one that went through cppyy and broke it out of pyexactreal eventually. We have not done much benchmarking yet, however, there is certainly a lot of room for improvement<sup>1</sup>.

```
>>> import gmpxxyy, gmpy2
>>> a = gmpxxyy.mpz(1)
>>> %timeit a + a
1.34 µs ± 5.16 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
>>> a = gmpy2.mpz(1)
>>> %timeit a + a
57.3 ns ± 0.28 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
```

As another downside we have [cppyy](https://cppyy.readthedocs.io/) as a dependency which at the time of this writing is a very heavy one indeed.

## Current Release Info

We build and release this package with every push to the master branch. These releases are considered unstable and highly
experimental. There are no stable releases yet.

This repository contains:

* **gmpxxyy** a Python wrapper for **libgmpxx**

| Name | Downloads | Version | Platforms |
| --- | --- | --- | --- |
| [![Nightly Build](https://img.shields.io/badge/recipe-gmpxxyy-green.svg)](https://anaconda.org/flatsurf/gmpxxyy) | [![Conda Downloads](https://img.shields.io/conda/dn/flatsurf/gmpxxyy.svg)](https://anaconda.org/flatsurf/gmpxxyy) | [![Conda Version](https://img.shields.io/conda/vn/flatsurf/gmpxxyy.svg)](https://anaconda.org/flatsurf/gmpxxyy) | [![Conda Platforms](https://img.shields.io/conda/pn/flatsurf/gmpxxyy.svg)](https://anaconda.org/flatsurf/gmpxxyy) |

## Install with Conda

You can install this package with conda. Download and install [Miniconda](https://conda.io/miniconda.html), then run

```
conda config --add channels conda-forge
conda create -n gmpxxyy -c flatsurf gmpxxyy
conda activate gmpxxyy
```

## Run with binder in the Cloud

You can try out this project in a very limited environment online by clicking this link:

* **gmpxxyy** [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/flatsurf/exact-real/master?filepath=doc%2Fbinder%2FSample.gmpxxyy.ipynb)

## Build from the Source Code Repository

We are following an autoconf setup, i.e., you can install `src/gmpxxyy` with
the following:

```
git clone --recurse-submodules https://github.com/flatsurf/gmpxxyy.git
cd gmpxxyy
./bootstrap
./configure
make
make check # to run our test suite
make install # to install into /usr/local
```

## Maintainers

* [@saraedum](https://github.com/saraedum)

---

<sup>1</sup> These benchmarks are not tuned in any way. I just typed them into a Python REPL on my Laptop with conda's IPython. This is not meant to be exact in any way, just to give you a very rough sense of what to expect. If I should really be benchmarking something else instead, please let me know :)
