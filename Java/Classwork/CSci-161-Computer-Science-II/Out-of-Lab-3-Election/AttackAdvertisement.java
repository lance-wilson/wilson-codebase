/**
 * The AttackAdvertisement Class is used to store data for an attack advertisement.  
 * An AttackAdvertisement has a target.
 * AttackAdvertisement is a subclass of Advertisement.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */

import java.util.Random;

public class AttackAdvertisement extends Advertisement
{
    private Candidate target = new Candidate();
    Random rand = new Random();

    /**
     * Default constructor calls the default Advertisement superclass constructor and then sets the type to 1 (the identifier for Attack Advertisements).
     */
    public AttackAdvertisement()
    {
        super();
        setType(1);
        setCost(rand.nextInt(25001)+50000);
        setTarget(new Candidate());
    }

    /**
     * Parameter instructor takes in two candidates. The first is sent to the Advertisement superclass constructor, while the second is set as a target. The cost is set between 50000 and 75000, and the type is set to 1 (the identifier for Attack Advertisements.
     * @param inCandidate1 is the candidate running the advertisement.
     * @param inCandidate2 is the target candidate.
     * @exception OutOfMoneyException is thrown if the candidate doesn't have enough money to pay for the advertisement.
     */
    public AttackAdvertisement(Candidate inCandidate1, Candidate inCandidate2) throws OutOfMoneyException
    {
        super(inCandidate1);
        setCost(rand.nextInt(25001)+50000);
        if (inCandidate1.getMoney() < getCost())
        {
            throw new OutOfMoneyException();
        }
        setTarget(inCandidate2);
        setType(1);
    }

    /**
     * The setTarget sets the input candidate as the target of the attack of advertisement.
     * @param inTarget is the candidate set as the target
     */
    public void setTarget(Candidate inTarget)
    {
        target = new Candidate(inTarget);
    }

    /**
     * The getTarget method allows access to the target candidate.
     * @return the target candidate.
     */
    public Candidate getTarget()
    {
        return target;
    }

    /**
     * The approval method checks to see if the candidate prefers the attack advertisement, and changes the debate and money modifiers for the candidate and the target depending on the result of this approval.
     * @return the string of whether the message was approved.
     */
    public String approval()
    {
        if (getCandidate().endorsement(new AttackAdvertisement()))
        {
            getCandidate().setDebateMod(0.2);
            getCandidate().setMoneyMod(-0.2);
            getTarget().setDebateMod(-0.15);
            getTarget().setMoneyMod(-0.25);
            return "My name is " + getCandidate().getName() + ", and I approve this message.";
        }
        else
        {
            getCandidate().setDebateMod(0.1);
            getCandidate().setMoneyMod(-0.05);
            getTarget().setDebateMod(-0.05);
            getTarget().setMoneyMod(-0.1);
            return "This message has not been approved by " + getCandidate().getName() + ".";
        }
    }

    /**
     * The toString method returns a string giving information about this advertisement.
     * @return the information string.
     */
    public String toString()
    {
        return "This attack advertisement run by " + getCandidate().getName() + " and targeting " + getTarget().getName() + " has a cost of " + getCost() + "\nCandidate's approval: " + approval() + "\n";
    }

}
