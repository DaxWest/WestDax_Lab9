# traffic - Program to solve the generalized Burger
# equation for the traffic at a stop light problem

#Repository link: https://github.com/DaxWest/WestDax_Lab9.git

# Set up configuration options and special features
import numpy as np
import matplotlib.pyplot as plt

#initial parameters
method = 2 #corresponding integers are 1) FTCS, 2) Lax, 3) Lax-Wendroff
N = 600 #number of grid points
L = 1200  # System size (meters)
h = L / N  # Grid spacing for periodic boundary conditions
v_max = 25.  # Maximum car speed (m/s)
tau = h/v_max #timestep
nstep = 1500 #number of steps
rho_max = 1.0  # Maximum density

def eqn_advection(method, N, h, tau, v_max, rho_max):
    '''

    :param method: Different possible solution methods. Note: only Lax method gives a valid answer
    :param N: Number of grid points
    :param h: Grid spacing for periodic boundary conditions
    :param tau: Time step
    :param v_max: Maximum speed of "objects"
    :param rho_max: Maximum density of "objects"
    :return: tplot, iplot, rplot, xplot
    '''
    coeff = tau / (2 * h)  # Coefficient used by all schemes
    coefflw = tau ** 2 / (2 * h ** 2)  # Coefficient used by Lax-Wendroff

    # * Set initial and boundary conditions
    Flow_max = 0.25 * rho_max * v_max  # Maximum Flow
    Flow = np.empty(N)
    cp = np.empty(N)
    cm = np.empty(N)
    # Initial condition is a square pulse from x = -L/4 to x = 0
    rho = np.zeros(N)
    for i in range(int(N / 4), int(N / 2)):
        rho[i] = rho_max  # Max density in the square pulse

    rho[int(N / 2)] = rho_max / 2  # Try running without this line

    # Use periodic boundary conditions
    ip = np.arange(N) + 1
    ip[N - 1] = 0  # ip = i+1 with periodic b.c.
    im = np.arange(N) - 1
    im[0] = N - 1  # im = i-1 with periodic b.c.

    # * Initialize plotting variables.
    iplot = 1
    xplot = (np.arange(N) - 1 / 2.) * h - L / 2.  # Record x for plot
    rplot = np.empty((N, nstep + 1)) # Record density for plot
    tplot = np.empty(nstep + 1) # Record time for plot
    rplot[:, 0] = np.copy(rho)  # Record the initial state
    tplot[0] = 0  # Record the initial time (t=0)

    # * Loop over desired number of steps.
    for istep in range(nstep):

        # * Compute the flow = (Density)*(Velocity)
        Flow[:] = rho[:] * (v_max * (1 - rho[:] / rho_max))

        # * Compute new values of density using
        #  FTCS, Lax or Lax-Wendroff method.
        if method == 1:  ### FTCS method ### #this method does not currently work
            rho[:] = rho[:] - coeff * (Flow[ip] - Flow[im])
        elif method == 2:  ### Lax method ###
            rho[:] = 0.5 * (rho[ip] + rho[im]) - coeff * (Flow[ip] - Flow[im])
        else:  ### Lax-Wendroff method ### #this method does not currently work
            cp[:] = v_max * (1 - (rho[ip] + rho[:]) / rho_max);
            cm[:] = v_max * (1 - (rho[:] + rho[im]) / rho_max);
            rho[:] = rho[:] - coeff * (Flow[ip] - Flow[im]) + coefflw * (
                    cp[:] * (Flow[ip] - Flow[:]) - cm[:] * (Flow[:] - Flow[im]))

        # * Record density for plotting.
        rplot[:, iplot] = np.copy(rho)
        tplot[iplot] = tau * (istep + 1)
        iplot += 1
    return tplot, iplot, rplot, xplot

#using the function to get the values for plotting
tplot, iplot, rplot, xplot = eqn_advection(method, N, h, tau, v_max, rho_max)

#plotting
fig = plt.figure()
# Graph of snapshots of density versus position
time = np.linspace(0, nstep, 5, True)
for i in time: #loop to show snapshots
    plt.plot(xplot, rplot[:,int(i)], label=f'time = {i*tau}s')
plt.title('Snapshot of Position vs Density for Given Time')
plt.xlabel('Position (x)')
plt.ylabel('Density (rho)')
plt.legend()
plt.show()

# Graph contours of density versus position and time.
levels = np.linspace(0., 1., num=11)
ct = plt.contour(xplot, tplot, np.flipud(np.rot90(rplot)), levels)
plt.clabel(ct, fmt='%1.2f')
plt.xlabel('Position (x)')
plt.ylabel('Time (t)')
plt.title('Density Contours for Position vs Time')
plt.show()