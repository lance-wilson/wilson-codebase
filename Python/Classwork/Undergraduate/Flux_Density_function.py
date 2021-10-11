# Lance Wilson
# AtSc 345
# Purpose: Function calculates the flux density at the planet given its distance from the sun.
# Modification History:
#   2016/09/08 - Lance Wilson: Written.

def flux_calc(r_planet):
    r_sun = 700000.
    flux_sun = 62831853.

    planet_flux = flux_sun * ((r_sun)**2/(r_planet)**2)
    return planet_flux
