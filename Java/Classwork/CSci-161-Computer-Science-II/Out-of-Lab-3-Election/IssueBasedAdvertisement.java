/**
 * The IssueBasedAdvertisement class is used to store data and methods related to an Issue Based Advertisement.  
 * The IssueBasedAdvertisement is a subclass of Advertisement.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */

import java.util.Random;

public class IssueBasedAdvertisement extends Advertisement
{
    Random rand = new Random();

    /**
     * Default constructor calls the default Advertisement superclass constructor and sets the type to 0 (the identifier for Issue Based advertisements
     */
    public IssueBasedAdvertisement()
    {
        super();
        setType(0);
        setCost(rand.nextInt(15001)+5000);
    }

    /**
     * Parameter constructor takes in a candidate, uses the Advertisement constructor to set that candidate, and sets the cost between 5000 and 20000.
     * @param inCandidate is the candidate paying for the advertisement.
     */
    public IssueBasedAdvertisement(Candidate inCandidate) throws OutOfMoneyException
    {
        super(inCandidate);
        setCost(rand.nextInt(15001)+5000);
        if (inCandidate.getMoney() < getCost())
        {
            throw new OutOfMoneyException();
        }
        setType(0);
    }

    /**
     * The approval method checks to see if the candidate prefers the issue based advertisement, and changes the debate modifier for the candidate depending on the result of this approval.
     * @return the string of whether the message was approved.
     */
    public String approval()
    {
        if (getCandidate().endorsement(new IssueBasedAdvertisement()))
        {
            getCandidate().setDebateMod(0.1);
            return "My name is " + getCandidate().getName() + ", and I approve this message.";
        }
        else
        {
            getCandidate().setDebateMod(0.05);
            return "This message has not been approved by " + getCandidate().getName() + ".";
        }
    }

    /**
     * The toString method returns a string giving information about this advertisement.
     * @return the information string.
     */
    public String toString()
    {
        return "This issue based advertisement has a cost of " + getCost() + ".\nCandidate approval: " + approval() + "\n";
    }

}
