/**
 * The Car class stores data and methods pertaining to a car.
 * A car has a mileage, a registration number, a description, and a fuel guage. The class of Car has a static registration number to make sure each car has a different registration number.
 * The Car class requires the FuelGauge class.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 4
 */

public class Car
{
    private int mileage = 0;  // Mileage of the car
    private int thisReg = 0;  // Registration of this car
    private static int regNumber = 0;  // Registration common to all cars.
    private String description = "";   // Description of car
    private FuelGauge fuelGauge = new FuelGauge();  // The car's fuel gauge.

    /**
     * The default constructor sets the registration number, sets the mileage equal to 0, and creates a new fuel gauge.
     */
    public Car()
    {
        setRegistration();
        setMileage(0);
        fuelGauge = new FuelGauge();
    }

    /**
     * Parameter constructor takes in a car and copies the data over.
     * @param inCar is the Car to be copied.
     */
    public Car(Car inCar)
    {
        setMileage(inCar.getMileage());
        setRegistration();
        setFuelGauge(inCar.getFuelGauge());
    }

    /**
     * setMileage sets the value of the car's mileage to the inputted value.
     * @param inMileage is the value set to the car's mileage.
     */
    public void setMileage(int inMileage)
    {
        mileage = inMileage;
    }

    /**
     * addMileage adds the input value to the mileage to the car.
     * @param inMileage is the mileage to add to the car.
     */
    public void addMileage(int inMileage)
    {
        mileage += inMileage;
    }

    /**
     * getMileage allows access to the cars mileage. Will return 0 if the mileage is less than 0.
     * @return the mileage of the car.
     */
    public int getMileage()
    {
        if (mileage < 0)
        {
            return 0;
        }
        else
        {
            return mileage;
        }
    }

    /**
     * setRegistration sets the registration number of this car, and increments the registration common to all cars.
     */
    private void setRegistration()
    {
        thisReg = regNumber;
        regNumber++;
    }

    /**
     * getRegistration allows access to this car's registration number.
     * @return the registration number of this car.
     */
    public int getRegistration()
    {
        return thisReg;
    }

    /**
     * setFuelGauge is used to copy a fuel gauge over to a copied car.
     * @param inFuelGauge is the fuel gauge to be copied over.
     */
    public void setFuelGauge(FuelGauge inFuelGauge)
    {
        fuelGauge = new FuelGauge(inFuelGauge);
    }

    /**
     * getFuelGauge allows access to this car's fuel gauge.
     * @return the fuel gauge of this car.
     */
    public FuelGauge getFuelGauge()
    {
        return fuelGauge;
    }

    /**
     * drive checks whether the car has fuel left. If it doesn't, it prints that there is no gas left in the car. If there is fuel remaining, 25 miles are added to the car's mileage and 1 gallon of fuel is consumed.
     */
    public void drive()
    {
        if (fuelGauge.getCurrentFuel() > 0)
        {
            addMileage(25);
            getFuelGauge().consumeFuel(1);
        }
        else
        {
            System.out.println("No gas left in the car.");
        }
    }

    /**
     * equals takes in a car and checks if they have equal registration numbers.
     * @param inCar is the car to be checked against
     * @return a boolean stating whether the cars are equal.
     */
    public boolean equals(Car inCar)
    {
        boolean value;
        if (getRegistration() == inCar.getRegistration())
        {
            value = true;
        }
        else
        {
            value = false;
        }
        return value;
    }

    /**
     * toString returns the description string giving information about the car.
     * @return the string description.
     */
    public String toString()
    {
        description = "Car with registration number " + getRegistration() + " has the following attributes: " + "\n\tMileage: " + getMileage() + "\n\tFuel: " + getFuelGauge().getCurrentFuel() + "\n";
        return description;
    }
}
