/**
 * The PhoneFundraiser Class is used to store data and methods about a PhoneFundraiser.  
 * The PhoneFundraiser is a subclass of Fundraiser.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */

public class PhoneFundraiser extends Fundraiser
{
    /**
     * Default constructor calls the default Fundraiser superclass constructor.
     */
    public PhoneFundraiser()
    {
        super();
    }

    /**
     * Parameter Constructor takes in a candidate and a location and calls the Fundraiser parameter constructor to set those values.
     * @param inCandidate is the candidate running the fundraiser.
     * @param inLocation is the location of the fundraiser.
     */
    public PhoneFundraiser(Candidate inCandidate, String inLocation)
    {
        super(inCandidate, inLocation);
    }

    /**
     * changeMods runs a fundraiser and then modifies the candidates money modifiers.
     */
    public void changeMods()
    {
        fundraiser_act();
        getCandidate().setMoneyMod(-0.05);
    }

    /**
     * Returns a string that provides information about this fundraiser.
     * @return the information string
     */
    public String toString()
    {
        return "Phone Call Fundraiser at Location " + getLocation() + " with " + getDonors() + " donors held by " + getCandidate().getName() + " netted $" + getCandMoney() + " and decresed the candidate's money modifier by 0.05" + "\n";
    }

}
