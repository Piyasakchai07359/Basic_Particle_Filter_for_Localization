'''
This program create for education about particle filter localization in simply concept.

Assume aircraft is flying on somewhere that we unknow position of aircraft but aircraft 
can observe altitude of aircraft from ground surface and we have map of this area that aircraft is flying. 
We will use particle filter to localization position of aircraft.

'''
import numpy as np
import matplotlib.pyplot as plt

#########################################################################################
# Setting Parameter...
#########################################################################################
n_particles = 100 # Number of particle 
lower_bound = -10 # Lower bound of Area
upper_bound = 10  # Upper bound of Area
position_aircraft = -9 # Initial position of Aircreaft
n = 100 # Number of interval in Area 
number_per_step = 5 # Number of Stepsize to move 
altitude_of_aircraft_from_sea_level = 1200 # Altitude of Aircraft from sea level
sigma_of_moving = 0.5 # Standard Deviation of moving Aircraft 
sigma_of_observing = 30 # Standard Deviation of observing
sigma_of_resample_position_particles = 0.5 # Standard Deviation of resampling
number_operate = 10 # Number of loop that Operate
#########################################################################################

#########################################################################################
# Calculate Other Value...
#########################################################################################
x_values = np.linspace(lower_bound,upper_bound,n)
distance_step = abs(x_values[1]-x_values[0])
distance_moving = number_per_step*distance_step
altitude_of_aircraft_plot = altitude_of_aircraft_from_sea_level*np.ones(n_particles)
#########################################################################################

#########################################################################################
# Determine Function of Altitude...
#########################################################################################
def function_altitude(x):
    return (x**3) + (x**2)+(50*np.sin(20*x))
#########################################################################################

#########################################################################################
# Determine Function that use in Particle Filter for Localization...
#########################################################################################
def start_gen_position_particles():
    random_ratio_distance = np.random.rand(n_particles,1)
    distance_from_lower = random_ratio_distance*(upper_bound-lower_bound)
    position_particles = distance_from_lower+lower_bound
    return position_particles

def moving_aircraft(position_aircraft,distance_moving):
    distance_moving_noise = np.random.normal(distance_moving,sigma_of_moving,1)
    position_aircraft = position_aircraft+ distance_moving_noise 
    return position_aircraft

def moving_position_particles(position_particles, distance_moving):
    position_particles = position_particles+ distance_moving
    position_particles = np.clip(position_particles,lower_bound,upper_bound)
    return position_particles

def observing_altitude_aircraft(position_aircraft,mode_noise = False):
    altitude_aircraft = function_altitude(position_aircraft)
    if mode_noise:
        return np.random.normal(altitude_aircraft,sigma_of_observing,1)
    return altitude_aircraft

def calculate_weights(position_particles, altitude_aircraft):  
    altitude_errors = np.zeros(n_particles)
    for i in range(n_particles):
        observating_altitude_particles = observing_altitude_aircraft(position_particles[i],mode_noise = False)
        altitude_errors[i] = abs(altitude_aircraft[0] - observating_altitude_particles[0])
    weights = np.max(altitude_errors)-altitude_errors
    weights [ (position_particles[:,0] == lower_bound) |(position_particles[:,0] == upper_bound)] = 0.0
    calculated_weights = weights ** 4
    return calculated_weights

def resample_position_particle(position_particles, calculated_weights):
    calculated_probabilities = calculated_weights / np.sum(calculated_weights)
    new_index=np.random.choice(n_particles,size = n_particles,p = calculated_probabilities)
    position_particles = position_particles[new_index]
    noise = np.random.normal(0,sigma_of_resample_position_particles,n_particles)
    noise = np.reshape(noise,(n_particles, 1))
    position_particles = position_particles+noise
    return position_particles
#########################################################################################

#########################################################################################
# Main Function...
#########################################################################################
if __name__ == '__main__':
    y_values = function_altitude(x_values)
    fig,ax = plt.subplots()
    position_particles = start_gen_position_particles()
    for k in range(number_operate):
        position_aircraft = moving_aircraft(position_aircraft,distance_moving)
        position_particles = moving_position_particles(position_particles, distance_moving)
        altitude_aircraft = observing_altitude_aircraft(position_aircraft,mode_noise = True)
        calculated_weights = calculate_weights(position_particles, altitude_aircraft)
        position_particles = resample_position_particle(position_particles, calculated_weights)
        plt.plot(x_values,y_values, label='Surface')
        plt.title('Particle Filter Localization')
        plt.xlabel("Position")
        plt.ylabel("Altitude")
        plt.plot(position_particles, altitude_of_aircraft_plot, 'r+', label = 'particle')
        best_guess = np.mean(position_particles)
        plt.plot(best_guess, altitude_of_aircraft_from_sea_level, 'go', label = 'guess position')
        plt.plot(position_aircraft, altitude_of_aircraft_from_sea_level, 'yo', label = 'current position')
        plt.legend()
        plt.pause(1)
        plt.cla()
    plt.show()
    plt.close()
#########################################################################################