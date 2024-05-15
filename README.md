# Estimating the Movement of Charged Particle Near the Superconductor <br>
## I. Setting Up Differential Equations <br>
To get the force acting on a charge we will use method of images [1].<br>
- For a **moving charge q**, its vertically flipped image (assuming plane of Superconductor is aligned at **y=0**) is constructed, with the charge **-q**, as shown in the figure below. <br>
![image](/figures/figure1.png)<br>
- From that image, Induced Magnetic Field **B**, and hence the **Lorentz Force** acting on a particle can be determined:<br>
![image](/figures/MovingChargeB.jpg)<br>
![image](/figures/LorentzForce.png)

If we consider **Lorentz Force** always being normal to the velocity of the particle, then it's clear that the magnitude of particle's velocity doesn't change, only its direction, making gamma factor constant.<br>
- As the force being strictly normal to particle's velocity, means the acceleration being strictly normal just as well, the formula for **Relativistic Force** simplifies, cancelling the parallel term out: <br>
![image](/figures/RelativisticForce.png)<br>
- This means multiplying magnitude of **Lorentz Force** by the normal of the velocity, will yield the instantaneous **Lorentz Force** vector, from which **instantaneous acceleration** can be defined:<br>
![image](/figures/RelativisticAccelerations.png)<br>
- To complete the necessary setup, differential equations of **position** must be written, which are trivial:<br>
![image](/figures/Speeds.png)

From that, it is technically possible to numerically solve the position over time, but the values used in calculations will have vastly different magnitudes, which might bring numerical issues.

## II. Nondimensionalisation <br>
In order to avoid some values being inherently large (like speed and acceleration) while others are inherently tiny (like position), we should scale them by some characteristic value. <br>
- To keep values close to 1, velocities have been characterized by the **speed of light**, while positions by the **distance of closest approach** calculated for **Non-Relativistic** case. <br>
![image](/figures/Nondimensionalisation.png) <br>
- The formula for **distance of closest approach** calculated in **Non-Relativistic** case can be derived from the **Lorentz Force** and the fact that the Magnetic Field doesn't do any work. <br>
![image](/figures/MinApproachDistance.png) <br>
- From that, nondimensionalised accelerations can be derived, and constants grouped together. <br>
![image](/figures/NondimensionalisedAccelerations.png) <br>
- Then differential equation of **position** results as: <br>
![image](/figures/NondimensionalisedPositions.png) <br>

## III. Results <br>
We have implemented Midpoint Solver with NumPy's 64bit floating point numbers, and recording steps of particle near SC into dataframe. <br>
- For the 1252 MeV/c proton (0.8c) incident at 45 degrees to the SC plane, following plot has been produced: <br>
![image](/figures/proton_08_45_nonret.png)


As the proton approaches SC, it is being deflected along a symmetric elliptical trajectory, with distance of closest approach scaled by a factor of 1/gamma as compared to Non-Relativistic approach distance. <br>
If we then construct the graph of closest approach distance against angle of incidence for different particles, we should observe that for the Relativistic case, **distance of closest approach** does depend on the **speed of the particle** (contrary to Non-Relativistic one). <br>
- 1252 MeV/c proton (0.8c), 2859 MeV/c proton (0.95c) and 3659 MeV/c helium (0.7c), being shot at angles varying from 10 to 85 degrees.
![image](/figures/cosmicrays_approachdist.png)

## IV. Time Retardation <br>
In reality information travels with a limited speed - **c**, which means Induced Magnetic Field **B** will take some time to adjust to particle's position. Hence Lorentz Force is calculated for previous position of the particle. <br>
Determining exact **Time Difference** between current and previous position is not possible analytically. And while equation for Time Difference is pretty straightforward to define, and solution can be found using Search Algorithms, this would be computationally expensive to perform.
- Hence a much simplier estimate will be used:<br>
![image](/figures/deltaTime.png) <br>
![image](/figures/nondimensionalisedDeltaTime.png)
- **Radius vector** between previous image position and current particle position is given by:<br>
![image](/figures/chargeImageRetardedDistance.png)
- **Angle** between particle position and previous image velocity for calculating Induced B is given by:<br>
![image](/figures/velocityDistanceRetardedAngle.png)
- Substituting these into **Lorentz Force** and **Relativistic Acceleration** yields:<br>
![image](/figures/retardedAcceleration.png)
- D.E for **position** do not change:<br>
![image](/figures/NondimensionalisedPositions.png)

## V. Results with Time Retardation <br>
The same Midpoint Solver has been used, but now storing position and velocity on each step into a **queue**, in order to later fetch it.
- For the 1252 MeV/c proton (0.8c) incident at 45 degrees to the SC plane, following plot has been produced:<br>
![image](/figures/proton_08_45_ret.png)

Based on these results, **Time Retardation** appears to **reduce approach distance** even further, and bend trajectory in **asymmetric** way, with reflection angle being greater than incidence.<br>
It is worth noting that function used to approximate Time Difference always underestimates the actual value, which means both absolute values and curvature of trajectory in the above plot are inaccurate.<br>

## VI. Conclusion <br>
This simulation lets us conclude that the original formula for determining distance of closest approach in **Non-Relativistic** case does work and can give a good reference value. But taking **Relativity** into account, particles get closer to SC than it estimates, **minimum approach distance** does in fact depend on **particle's velocity** and can follow **asymetric trajectory** given the effect of **Time Retardation**.<br>
Please reference [main_notebook.ipynb](/main_notebook.ipynb) for the implementation. It also features cells for setting custom particle parameters and drawing these plots.

## References <br>
[1] Yang, Z. (1994). Focusing a charged-particle beam by a superconductor. Physica. C, Superconductivity, 230(3–4), 419–424. https://doi.org/10.1016/0921-4534(94)90860-5












