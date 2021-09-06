/**
 * The Advertisement Class is used to store data for an advertisement.  
 * An Advertisement has a cost, a type, and a candidate.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */

public class Advertisement
{
    private double cost;  // Cost
    private int type = -1;  // Type is integer identifier of each type. -1 is the default. Subclasses each have their own identifier.
    private Candidate candidate = new Candidate();
    private String message = "";

    /** 
     * Default Constructer, which provides starting cost only.
     */
    public Advertisement()
    {
        setCost(1000);
    }

    /** 
     * Parameter Constructor that takes in the candidate paying for the advertisement.
     * @param inCandidate becomes the candidate paying for the advertisement.
     * @exception OutOfMoney Exception is thrown if the candidate doesn't have the money to buy an advertisement.
     */
    public Advertisement(Candidate inCandidate) throws OutOfMoneyException
    {
        if (inCandidate.getMoney() < getCost())
        {
            throw new OutOfMoneyException();
        }
        setCandidate(inCandidate);
    }

    /** 
     * The setCost method sets the cost of the Adverisement. 
     * @param inCost is the value of this cost.
     */
    public void setCost(double inCost)
    {
        cost = inCost;
    }

    /**
     * getCost gives access to the advertisement's cost.
     * @return the cost of the Ad.
     */
    public double getCost()
    {
        return cost;
    }

    /** 
     * The setType method sets ad's identifier number. 
     * @param inType is the integer ad type identifier.
     */
    public void setType(int inType)
    {
        type = inType;
    }

    /**
     * getType gives access to the advertisement's type.
     * @return the identifier number.
     */
    public int getType()
    {
        return type;
    }

    /** 
     * The setCandidate method sets the candidate buying the advertisement. 
     * @param inCandidate is the candidate paying for the Ad.
     */
    public void setCandidate(Candidate inCandidate)
    {
        candidate = new Candidate(inCandidate);
    }

    /**
     * getCandidate gives access to the ad's candidate.
     * @return the ad's candidate.
     */
    public Candidate getCandidate()
    {
        return candidate;
    }

    /**
     * setMessage sets the message stating what the advertisement is about.
     * @param inMessage becomes the Advertisement's new message.
     */
    public void setMessage(String inMessage)
    {
        message = inMessage;
    }

    /**
     * getMessage allows access to the Advertisement's message
     * @return the Advertisement's messageg
     */
    public String getMessage()
    {
        return message;
    }

    /**
     * The toString method gives a string that tells about the advertisement.
     * @return the ad's candidate.
     */
    public String toString()
    {
       return "The Advertisement run by " + getCandidate().getName() + " has a cost of $" + getCost() + "\n";
    }

}
