/**
 * The Caravel class stores data and methods pertaining to a Caravel.
 * A Caravel has an amount of passengers and cargo and a maximum amount of passengers and cargo, and inherits a name from the Watercraft superclass.
 * Caravel requires the Watercraft class and implements the CruiseShip and CargoShip interfaces.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 5
 */

public class Caravel extends Watercraft implements CargoShip, CruiseShip
{
    int passengers = 0;
    int max_passengers = 0;
    int cargo = 0;
    int max_cargo = 0;

    /**
     * Parameter constructor takes in a name, maximum number of passengers, and a maximum amount of cargo, sets the name via the superclass constructor, and sets the maximum number of passengers and cargo using those set methods.
     * @param inName is the name of the Caravel.
     * @param inMaxPass is the maximum number of passengers the Caravel can hold.
     * @param inMaxCargo is the maximum amount of cargo the Caravel can hold.
     */
    public Caravel(String inName, int inMaxPass, int inMaxCargo)
    {
        super(inName);
        setMaxPass(inMaxPass);
        setMaxCargo(inMaxCargo);
    }

    /**
     * setMaxPass sets the value of the Caravel's maximum number of passengers to the inputted value.
     * @param inMaxPass is the value set to the Caravel's maximum number of passengers.
     */
    public void setMaxPass(int inMaxPass)
    {
        max_passengers = inMaxPass;
    }

    /**
     * getMaxPass returns the maximum number of passengers allowed on the Caravel
     * @return the maximum number of passengers.
     */
    public int getMaxPass()
    {
        return max_passengers;
    }

    /**
     * setPass sets the number of passengers to the inputted value if that would not exceed the maximum number of passengers allowed on the Caravel.
     * @param the number of passengers to set onboard the Caravel.
     */
    private void setPass(int inPassengers)
    {
        if (inPassengers <= getMaxPass())
        {
            passengers = inPassengers;
        }
    }

    /**
     * getPass returns the number of passengers currently on the Caravel.
     * @return the number of passengers on board the Caravel.
     */
    public int getPass()
    {
        return passengers;
    }

    /**
     * setMaxCargo sets the maximum amount of cargo that the Caravel can hold.
     * @param inMaxCargo is the maximum amount of cargo the ship can hold.
     */
    public void setMaxCargo(int inMaxCargo)
    {
        max_cargo = inMaxCargo;
    }

    /**
     * getMaxCargo returns the maximum amount of cargo the Caravel can hold.
     * @return the maximum number of pounds of cargo the Caravel can hold.
     */
    public int getMaxCargo()
    {
        return max_cargo;
    }

    /**
     * setCargo sets the number of pounds of cargo the inputted value if that would not exceed the maximum amount of cargo allowed on the Caravel.
     * @param the number of pounds of cargo to place onboard the Caravel.
     */
    private void setCargo(int inCargo)
    {
        if (inCargo <= getMaxCargo())
        {
            cargo = inCargo;
        }
    }

    /**
     * getCargo returns the number of pounds of cargo currently on the Caravel.
     * @return the amount of cargo on board the Caravel.
     */
    public int getCargo()
    {
        return cargo;
    }

    /**
     * embark takes in a possible number of passengers and places as many passengers as it can on board the Caravel, and returns the number of passengers on board.
     * @param posPass is the possible number of passengers trying to get on board.
     * @return onBoardPass is the number of passengers that made it on board.
     */
    public int embark(int posPass)
    {
        int onBoardPass = 0;
        if (posPass <= getMaxPass())
        {
            onBoardPass = posPass;
        }
        else
        {
            onBoardPass = getMaxPass();
        }

        setPass(onBoardPass);
        return onBoardPass;
    }

    /**
     * disembark removes all passengers from aboard the Caravel.
     * @return the number of passengers who disembarked.
     */
    public int disembark()
    {
        int onBoardPass = getPass();
        setPass(0);
        return onBoardPass;
    }

    /**
     * load takes in a possible number of pounds of cargo and places as much cargo as it can on board the Caravel, and returns the amount of cargo on board.
     * @param posCargo is the possible amount of cargo that could get put on board.
     * @return onBoardPass is the amount of cargo that was put on board.
     */
    public int load(int posCargo)
    {
        int onBoardCargo = 0;
        if (posCargo <= getMaxCargo())
        {
            onBoardCargo = posCargo;
        }
        else
        {
            onBoardCargo = getMaxCargo();
        }

        setCargo(onBoardCargo);
        return onBoardCargo;
    }

    /**
     * unload removes all cargo from aboard the Caravel.
     * @return the number of pounds of cargo removed from the Caravel.
     */
    public int unload()
    {
        int onBoardCargo = getCargo();
        setCargo(0);
        return onBoardCargo;
    }

}
