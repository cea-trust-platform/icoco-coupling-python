# ICoCo API - Version 2 (02/2021)

**WARNING: This API should not be changed!!**

ICoCo stands for **Interface for Code Coupling**. This is a norm that a code may choose
to implement to facilitate its coupling with other ICoCo-compliant codes.

See https://github.com/cea-trust-platform/icoco-coupling for full reference.

Practically ICoCo is provided as a main abstract C++ class (ICoCo::Problem) that a code has
to derive to implement the norm. This can be only a partial implementation as some methods
are not relevant to all the codes (especially the I/O methods of the API).

This package implements the abstract class {class}`icoco.problem.Problem` in Python following the
specifications of the c++ version.

The Python implementation proposed is based on {mod}`medcoupling` implementation for fields and {mod}`mpi4py` for MPI
communication. Nevertheless, it is possible to use other implementation of such concepts within this
package.
