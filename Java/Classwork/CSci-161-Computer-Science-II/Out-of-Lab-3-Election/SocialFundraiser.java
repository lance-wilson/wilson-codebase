/**
 * The SocialFundraiser Class is used to store data and methods about a SocialFundraiser.  
 * The SocialFundraiser is a subclass of Fundraiser.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */

public class SocialFundraiser extends Fundraiser
{
    /**
     * Default constructor calls the default Fundraiser superclass constructor.
     */
    public SocialFundraiser()
    {
        super();
    }

    /**
     * Parameter Constructor takes in a candidate and a location and calls the Fundraiser parameter constructor to set those values.
     * @param inCandidate is the candidate running the fundraiser.
     * @param inLocation is the location of the fundraiser.
     */
    public SocialFundraiser(Candidate inCandidate, String inLocation)
    {
        super(inCandidate, inLocation);
    }

    /**
     * changeMods runs a fundraiser and then modifies the candidates money modifiers.
     */
    public void changeMods()
    {
        fundraiser_act();
        getCandidate().setMoneyMod(0.1);
    }

    /**
     * Returns a string that provides information about this fundraiser.
     * @return the information string
     */
    public String toString()
    {
        return "Social Fundraiser at Location " + getLocation() + " with " + getDonors() + " donors held by " + getCandidate().getName() + " netted $" + getCandMoney() + " and increased the candidate's money modifier by 0.1" + "\n";
    }

}
