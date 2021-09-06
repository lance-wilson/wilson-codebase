/**
 * The Barge class stores data and methods pertaining to a Barge.
 * A Barge has an amount of cargo and an amount of max_cargo, and inherits a name from the Watercraft superclass.
 * Barge requires the Watercraft class and implements the CargoShip interface.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 5
 */

public class Barge extends Watercraft implements CargoShip
{
    int cargo = 0;
    int max_cargo = 0;

    /**
     * Parameter constructor takes in a name and a maximum amount of cargo, sets the name via the superclass constructor, and sets the maximum amount of cargo using that set method.
     * @param inName is the name of the Barge.
     * @param inMaxCargo is the maximum amount of cargo the Barge can hold.
     */
    public Barge(String inName, int inMaxCargo)
    {
        super(inName);
        setMaxCargo(inMaxCargo);
    }

    /**
     * setMaxCargo sets the maximum amount of cargo that the Barge can hold.
     * @param inMaxCargo is the maximum amount of cargo the ship can hold.
     */
    public void setMaxCargo(int inMaxCargo)
    {
        max_cargo = inMaxCargo;
    }

    /**
     * getMaxCargo returns the maximum amount of cargo the Barge can hold.
     * @return the maximum number of pounds of cargo the Barge can hold.
     */
    public int getMaxCargo()
    {
        return max_cargo;
    }

    /**
     * setCargo sets the number of pounds of cargo the inputted value if that would not exceed the maximum amount of cargo allowed on the Barge.
     * @param the number of pounds of cargo to place onboard the Barge.
     */
    private void setCargo(int inCargo)
    {
        if (inCargo <= getMaxCargo())
        {
            cargo = inCargo;
        }
    }

    /**
     * getCargo returns the number of pounds of cargo currently on the Barge.
     * @return the amount of cargo on board the Barge.
     */
    public int getCargo()
    {
        return cargo;
    }

    /**
     * load takes in a possible number of pounds of cargo and places as much cargo as it can on board the Barge, and returns the amount of cargo on board.
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
     * unload removes all cargo from aboard the Barge.
     * @return the number of pounds of cargo removed from the Barge.
     */
    public int unload()
    {
        int onBoardCargo = getCargo();
        setCargo(0);
        return onBoardCargo;
    }

}
