# ICoCo V3 example #

## Motivation ##

This case is designed to illustrate ICoCo V3. It seeks to exploit all the standard's possibilities while remaining as simple as possible.

## Models ##

We model two 1D channels cooling a heating plate.

In each channel we solve for enthalpy convection with a source term linear in the temperature difference with the plate:

```math
\rho_i \dfrac{\partial H_i}{\partial t} + G_i \dfrac{\partial H_i}{\partial z} = h_i (T_s - T_{fi})
```

For the plate, we have a kind of 0D model:

```math
C \dfrac{\partial T_s}{\partial t} = h_1 (T_f1 - T_s) + h_2 (T_f2 - T_s) + P
```

Here we have:
* $\rho_i$: fluid density of channel $i$. This is a constant and homogeneous value.
* $H_i$: enthalpy (per unit of mass) of the fluid in channel $i$. This is a function of the fluid temperate.
* $G_i = \rho_i v_i$ where $v_i$ is the speed of the fluid in channel $i$. This is a constant and homogeneous value.
* $h_i$: heat transfer coefficient between channel i and the plate. This is a function of the plate temperate.
* $T_s$: plate temperature.
* $T_{fi}$: fluid temperature in channel $i$.
* $C$: volumetric heat capacity of the plate. This is a constant and homogeneous value.
* $P$: volumetric power. It can depend on the position.

$\rho_i$, $v_i$, $C$ and $P$ are user parameters.

$H_i$ is provided as a function of $T_{fi}$. $h_1$ and $h_2$ are provided as functions of $T_s$.

## Solving methods ##

### Stationary ###

In order to solve for the stationary fluid temperature, we iterate on:

```math
H_i^{j} = H_i^{j-1} + dz / G_i * h_i^{j} (T_s^{j} - T_{fi}^{j})
```

Here $dz$ is the cell size (taken constant) and the superscript $j$ stands for the cell index.

The function providing $H_i$ as a function of $T_{fi}$ is then inverted using a Newton algorithm to compute a new guess for $T_{fi}^{j}$.

The stationary plate temperature is computed using, in each cell:

```math
T_s = \dfrac{h_1 T_f1 + h_2 T_f2 + P}{h_1 + h_2}
```

As $h_1$ and $h_2$ depend on $T_s$, iterations are needed.

In order to get the coupled solution, fluid and solid are solved iteratively until convergence.

### Transient ###

In transient mode, we use an explicit time-scheme for the fluid:

```math
\rho_i \dfrac{H_i^{j, n+1} - H_i^{j, n}}{dt} + G_i \dfrac{H_i^{j, n} - H_i^{j-1, n}}{dz} = h_i^{j, n+1} (T_s^{j, n+1} - T_{fi}^{j, n+1})
```

Here $n$ stands for the time-step number and $dt$ is the time-step size. Because we use the current fluid temperature in the source term, iterations are needed.

Similarly, we write for the plate:

```math
C \dfrac{T_s^{j, n+1} - T_s^{j, n}}{dt} = h_1^{j, n+1} (T_f1^{j, n+1} - T_s^{j, n+1}) + h_2^{j, n+1} (T_f2^{j, n+1} - T_s^{j, n+1}) + P
```

Because in the source term $h_i$ depends on the plate temperature, and because we want to use the current plate temperature to compute it, iterations are needed.

In order to get the coupled solution, fluid and solid are solved iteratively until convergence.
