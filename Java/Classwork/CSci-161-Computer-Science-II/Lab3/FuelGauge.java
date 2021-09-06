/**
 * The FuelGauge class stores data and methods pertaining to a fuel gauge.
 * A Fuel Gauge has a current fuel level and a maximum fuel level.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 4
 */
import java.util.Random;

public class FuelGauge
{
    private int fuel_current = 0;  // Current level of fuel in tank.
    private int fuel_max = 0;      // Tank's capacity.
    Random rand = new Random();

    /**
     * The default constructor sets the level of max_fuel to a random integer between 15 and 25 (both inclusive), and creates a current fuel level within the tank's capacity.
     */
    public FuelGauge()
    {
        int max_fuel = rand.nextInt(11) + 15;
        setMaxFuel(max_fuel);
        setCurrentFuel(rand.nextInt(max_fuel));
    }

    /**
     * Parameter constructor takes in a FuelGauge and copies the data over.
     * @param inFuelGauge is the FuelGauge to be copied.
     */
    public FuelGauge(FuelGauge inFuelGauge)
    {
        setMaxFuel(inFuelGauge.getMaxFuel());
        setCurrentFuel(inFuelGauge.getCurrentFuel());        
    }

    /**
     * setCurrentFuel sets the value of current fuel, but only if it is between 0 and the maximum fuel value.
     * @param inCurrentFuel is the value to set as the current fuel
     */
    public void setCurrentFuel(int inCurrentFuel)
    {
        if (inCurrentFuel < 0)
        {
            System.out.println("Current fuel cannot be less than 0.");
        }
        else if (inCurrentFuel > getMaxFuel())
        {
            System.out.println("Current fuel cannot be greater than maximum fuel.");
        }
        else
        {
            fuel_current = inCurrentFuel;
        }
    }

    /**
     * consumeFuel subtracts fuel from the tank if there is gas remaining in the tank.
     * @param inFuel is the amount of fuel to subtract from the tank
     */
    public void consumeFuel(int inFuel)
    {
        if (fuel_current <= 0)
        {
            System.out.println("No gas left in the car to be consumed.");
        }
        else
        {
            fuel_current -= inFuel;
        }
    }

    /**
     * getCurrentFuel gives access to the value of fuel_current.
     * @return the value of fuel_current
     */
    public int getCurrentFuel()
    {
        return fuel_current;
    }

    /**
     * setMaxFuel sets the value of the maximum fuel, but only if it is not less than 0.
     * @param inMaxFuel is the level to set as the maximum amount of fuel.
     */
    public void setMaxFuel(int inMaxFuel)
    {
        if (inMaxFuel < 0)
        {
            System.out.println("Maximum fuel cannot be less than 0.");
        }
        else
        {
            fuel_max = inMaxFuel;
        }
    }

    /**
     * getMaxFuel allows access to the value of fuel_max.
     * @return the value of fuel_max.
     */
    public int getMaxFuel()
    {
        return fuel_max;
    }

    /**
     * compareTo takes in a fuel gauge and compares the percentage of fuel left in that fuel gauge to the percentage of fuel left in this fuel gauge. Returns a positive value if this fuel gauge has a greater percentage left, 0 if they percentages are equal, and a negative value if this fuel gauge has a smaller percentage left.
     * @param inFuelGauge is the fuel gauge to be compared to
     * @return the value designating which has the greater percentage left.
     */
    public int compareTo(FuelGauge inFuelGauge)
    {
        if (((float)getCurrentFuel())/getMaxFuel() > ((float)inFuelGauge.getCurrentFuel())/inFuelGauge.getMaxFuel())
        {
            return 1;
        }
        else if (((float)getCurrentFuel())/getMaxFuel() == ((float)inFuelGauge.getCurrentFuel())/inFuelGauge.getMaxFuel())
        {
            return 0;
        }
        else
        {
            return -1;
        }
    }

    /**
     * toString returns a string giving information on the fuel gauge
     * @return the string containing information.
     */
    public String toString()
    {
        return "This Fuel Gauge has:\n\tA current fuel level of: " + getCurrentFuel() + "\n\tA maximum fuel level of: " + getMaxFuel() + "\n";
    }
}
