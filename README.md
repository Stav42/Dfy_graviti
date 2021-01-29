# Dfy_graviti
Internship - Space Gravity simulator.

Simulation.py contains the code. I have used __scipy.integrate.solve_ivp__ function with the integrators listed below.

Results for different propagators are in __/Results__ Folder

## Integration methods used:

* __RK45__ (default): Explicit Runge-Kutta method of order 5(4) [1]. The error is controlled assuming accuracy of the fourth-order method, but steps are taken using the fifth-order accurate formula (local extrapolation is done). A quartic interpolation polynomial is used for the dense output [2]. Can be applied in the complex domain.

* __RK23__: Explicit Runge-Kutta method of order 3(2) [3]. The error is controlled assuming accuracy of the second-order method, but steps are taken using the third-order accurate formula (local extrapolation is done). A cubic Hermite polynomial is used for the dense output. Can be applied in the complex domain.

* __DOP853__: Explicit Runge-Kutta method of order 8 [13]. Python implementation of the “DOP853” algorithm originally written in Fortran [14]. A 7-th order interpolation polynomial accurate to 7-th order is used for the dense output. Can be applied in the complex domain.

* __Radau__: Implicit Runge-Kutta method of the Radau IIA family of order 5 [4]. The error is controlled with a third-order accurate embedded formula. A cubic polynomial which satisfies the collocation conditions is used for the dense output.

* __BDF__: Implicit multi-step variable-order (1 to 5) method based on a backward differentiation formula for the derivative approximation [5]. The implementation follows the one described in [6]. A quasi-constant step scheme is used and accuracy is enhanced using the NDF modification. Can be applied in the complex domain.

* __LSODA__: Adams/BDF method with automatic stiffness detection and switching [7], [8]. This is a wrapper of the Fortran solver from ODEPACK.

### Radius Magnitude (from origin) vs time plot for time period (0,65) (in seconds)

![image](https://github.com/Stav42/Dfy_graviti/blob/main/Propagators.png)

Magnified to (8-12) interval

![image](https://github.com/Stav42/Dfy_graviti/blob/main/8%20sec%20-%2012%20sec.png)
