/**
 * The TownHallAdvertisement class is used to store data and methods related to an Issue Based Advertisement.
 * A TownHallAdvertisement has a number of attendees.  
 * The TownHallAdvertisement is a subclass of Advertisement.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */

import java.util.Random;

public class TownHallAdvertisement extends Advertisement
{
    private int attendees = 0;
    Random rand = new Random();
    
    /**
     * Default constructor calls the default Advertisement superclass constructor and sets the type to 2 (the identifier for Town Hall advertisements
     */
    public TownHallAdvertisement()
    {
        super();
        setType(2);
        setCost(rand.nextInt(95001)+5000);
        setAttendance();
    }

    /**
     * Parameter constructor takes in a candidate, uses the Advertisement constructor to set that candidate, and sets the cost between 5000 and 100000.
     * @param inCandidate is the candidate paying for the advertisement.
     * @exception OutOfMoneyException is thrown if the candidate cannot afford this advertisement.
     */
    public TownHallAdvertisement(Candidate inCandidate) throws OutOfMoneyException
    {
        super(inCandidate);
        setCost(rand.nextInt(95001)+5000);
        if (inCandidate.getMoney() < getCost())
        {
            throw new OutOfMoneyException();
        }
        setAttendance();
        setType(2);
    }

    /**
     * setAttendance sets the number of attendees at the town hall.
     */
    private void setAttendance()
    {
        attendees = rand.nextInt(151);
    }

    /**
     * getAttendance allows access to the number of attendees.
     * @return the number of attendees.
     */
    public int getAttendance()
    {
        return attendees;
    }

    /**
     * The approval method checks to see if the candidate prefers the town advertisement, and changes the money modifier for the candidate depending on the result of this approval.
     */
    public String approval()
    {
        if (getCandidate().endorsement(new TownHallAdvertisement()))
        {
            getCandidate().setMoneyMod(getAttendance()/500.0);
           return getCandidate().getName() + " holds a successful Town Hall.";
        }
        else
        {
            getCandidate().setMoneyMod(getAttendance()/2000.0);
            return getCandidate().getName() + " holds a Town Hall.";
        }
    }

    /**
     * The toString method returns a string giving information about this advertisement.
     * @return the information string.
     */
    public String toString()
    {
        return "This town hall advertisement has a cost of $" + getCost() + " and an attendance of " + getAttendance() + "\nCandidate approval: " + approval() + "\n";
    }
}
