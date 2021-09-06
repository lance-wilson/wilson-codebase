/**
 * The Yacht class stores data and methods pertaining to a Yacht.
 * A Yacht has an amount of passengers and a maximum amount of passengers, and inherits a name from the Watercraft superclass.
 * Yacht requires the Watercraft class and implements the CruiseShip interface.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 5
 */

public class Yacht extends Watercraft implements CruiseShip
{
    int passengers = 0;
    int max_passengers = 0;

    /**
     * Parameter constructor takes in a name and maximum number of passengers, sets the name via the superclass constructor, and sets the maximum number of passengers using that set method.
     * @param inName is the name of the Yacht.
     * @param inMaxPass is the maximum number of passengers the Yacht can hold.
     */
    public Yacht(String inName, int inMaxPass)
    {
        super(inName);
        setMaxPass(inMaxPass);
    }

    /**
     * setMaxPass sets the value of the Yacht's maximum number of passengers to the inputted value.
     * @param inMaxPass is the value set to the Yacht's maximum number of passengers.
     */
    public void setMaxPass(int inMaxPass)
    {
        max_passengers = inMaxPass;
    }

    /**
     * getMaxPass returns the maximum number of passengers allowed on the Yacht
     * @return the maximum number of passengers.
     */
    public int getMaxPass()
    {
        return max_passengers;
    }

    /**
     * setPass sets the number of passengers to the inputted value if that would not exceed the maximum number of passengers allowed on the Yacht.
     * @param the number of passengers to set onboard the Yacht.
     */
    private void setPass(int inPassengers)
    {
        if (inPassengers <= getMaxPass())
        {
            passengers = inPassengers;
        }
    }

    /**
     * getPass returns the number of passengers currently on the Yacht.
     * @return the number of passengers on board the Yacht.
     */
    public int getPass()
    {
        return passengers;
    }

    /**
     * embark takes in a possible number of passengers and places as many passengers as it can on board the Yacht, and returns the number of passengers on board.
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
     * disembark removes all passengers from aboard the Yacht.
     * @return the number of passengers who disembarked.
     */
    public int disembark()
    {
        int onBoardPass = getPass();
        setPass(0);
        return onBoardPass;
    }

}
