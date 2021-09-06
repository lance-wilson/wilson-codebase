/**
 * The PACFundraiser Class is used to store data and methods about a PACFundraiser.  
 * The PACFundraiser is a subclass of Fundraiser.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #3
 */

public class PACFundraiser extends Fundraiser
{
    /**
     * Default constructor calls the default Fundraiser superclass constructor.
     */
    public PACFundraiser()
    {
        super();
    }

    /**
     * Parameter Constructor takes in a candidate and a location and calls the Fundraiser parameter constructor to set those values.
     * @param inCandidate is the candidate running the fundraiser.
     * @param inLocation is the location of the fundraiser.
     * @exception TooLowInPollsException is thrown if the candidate doesn't have enough money to run a PAC fundraiser.
     */
    public PACFundraiser(Candidate inCandidate, String inLocation) throws TooLowInPollsException
    {
        super(inCandidate, inLocation);
        if(inCandidate.getMoney() < 0.01 * inCandidate.getTotalMoney())
        {
            throw new TooLowInPollsException();
        }
    }

    /**
     * changeMods runs a fundraiser and then modifies the candidates debate and money modifiers.
     */
    public void changeMods()
    {
        fundraiser_act();
        getCandidate().setMoneyMod(0.2);
        getCandidate().setDebateMod(0.1);
    }

    /**
     * Returns a string that provides information about this fundraiser.
     * @return the information string
     */
    public String toString()
    {
        return "PAC Fundraiser at Location " + getLocation() + " with " + getDonors() + " donors held by " + getCandidate().getName() + " netted $" + getCandMoney() + " and increased the candidate's money modifier by 0.2 and the candidate's debate modifier by 0.1" + "\n";
    }

}
