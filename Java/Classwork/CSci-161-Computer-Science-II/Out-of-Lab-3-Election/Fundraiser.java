/**
 * The Fundraiser Class is used to simulate a fundraiser for a single candidate.  
 * A fundraiser has a location, donors, candidates, and a fundraiser method.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #3
 */

import java.util.Random;

public class Fundraiser
{
    private String location = "";
    private double candidate_money;
    private int donors;
    protected Random randomNum = new Random();
    private Candidate candidate = new Candidate();

    /**
     * Default constructor creates a fundraiser with a location of Hill Number 1, Alabama, and a random number of donors.
     */
    public Fundraiser()
    {
        location = "Hill Number 1, Alabama";
        donors = randomNum.nextInt(201);
    }

    /**
     * Parameter constructor creates a fundraiser at the location provided with the provided candidate.
     * @param inLocation is the location of the debate.
     * @param inCandidate is the candidate holding the fundraiser.
     */
    public Fundraiser(Candidate inCandidate, String inLocation)
    {
        location = inLocation;
        setCandidate(inCandidate);
        donors = randomNum.nextInt(201);
    }

    /**
     * setLocation sets the fundraiser's location.
     * @param inLocation is a string that becomes the new location for the fundraiser.
     */
    public void setLocation(String inLocation)
    {
        location = inLocation;
    }

    /**
     * getLocation allows access to the fundraiser's location.
     * @return location is the fundraiser's current location.
     */
    public String getLocation()
    {
        return location;
    }

    /**
     * setCandidates sets the fundraiser's candidates.
     * @param inCandidate is the ArrayList of candidates entering the election.
     */
    public void setCandidate(Candidate inCandidate)
    {
        candidate = inCandidate;
    }

    /**
     * getCandidate allows access to the ArrayList of candidates.
     * @return the ArrayList of candidates.
     */
    public Candidate getCandidate()
    {
        return candidate;
    }

    /**
     * getDonors allows access to the fundraiser's number of donors.
     * @return the number of donors.
     */
    public int getDonors()
    {
        return donors;
    }

    /**
     * getCandMoney allows access to the fundraiser's candidate's raised money.
     * @return the amount of money raised.
     */
    public double getCandMoney()
    {
        return candidate_money;
    }

    /**
     * fundraiser_act simulates a fundraiser simulates a fundraiser with a randomly selected number of donors between 0 and 200, each of whom donates from $0 to $150.
     */
    public void fundraiser_act()
    {
        double donation = 0;
        double total = 0;
        int j;

        for (j = 0; j < getDonors(); j++)
        {
            // Randomly generate a donation for this donor.
            donation = randomNum.nextDouble()*150;
            // Add to running total
            total = total + donation;
            //System.out.println("Donor " + (j+1) + " donated $" + donation);
        }

        total = total * getCandidate().getMoneyMod();
        candidate_money = total;
        // Add money to the candidate's total.
        getCandidate().addMoney(total);
        System.out.println(getCandidate().getName() + " held a fundraiser at " + getLocation() + " and raised $" + total + " for a total of $" + getCandidate().getMoney());
        return;
    }

    /**
     * Returns a string that provides information about the fundraiser.
     * @return the information string
     */
    public String toString()
    {
        return "Fundraiser at Location " + getLocation() + " with " + getDonors() + " held by " + getCandidate().getName() + " netted $" + candidate_money + "\n";
    }

}
