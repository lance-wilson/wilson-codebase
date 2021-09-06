/**
 * The Candidate Class is used to simulate candidate for the election.  
 * A Candidate has a name, a slogan, a political party, money, a money modifier, a debate modifier, and preferences for advertisments and fundraisers.
 * There is also a static value of the total money in play.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */
import java.util.Random;

public class Candidate implements Comparable<Candidate>
{
 
    private String name = "";   //Name of mouse
    private String slogan = ""; //Candidate's slogan
    private String party = "";  //Political Party
    private double money = 0.0;      //default money
    private double money_mod = 1.0;  //Default money modifier
    private double debate_mod = 1.0; // Default Debate modifier
    private int ad_prefer = 0;  //Advertisement preference
    final int number_ads = 3;   // Number of ad types
    private int fund_prefer = 0; //Fundraiser preference
    final int number_fundraisers = 3;   // Number of fundraiser types
    private static double total_money = 0.0;  //Total money in play
    private Random randomNum = new Random();

    /** 
     * Default Constructer, which provides starting money only.
     */
    public Candidate()
    {
        setName("Defacto");
        setSlogan("Vote for me!");
        setParty("Unexpected Party");
        money = randomNum.nextInt(101);
        total_money += money;
        setAdPrefer();
        setFundPrefer();
    }

    /** 
     * Parameter Constructor that takes in a name, party, and slogan and sets them to the values of name, party, and slogan.
     * @param inName becomes the name of the candidate.
     * @param inParty becomes the party of the candidate.
     * @param inSlogan becomes the slogan of the candidate.
     */
    public Candidate(String inName, String inParty, String inSlogan)
    {
        name = inName;
        party = inParty;
        slogan = inSlogan;
        money = randomNum.nextInt(101);
        total_money += money;
        setAdPrefer();
        setFundPrefer();
    }

    /** 
     * Parameter Constructor that takes in a name, party, and slogan and sets them to the values of name, party, and slogan.
     * @param inName becomes the name of the candidate.
     * @param inParty becomes the party of the candidate.
     * @param inSlogan becomes the slogan of the candidate.
     * @param inAdPrefer becomes the ad preference.
     * @param inFundPrefer becomes the fundraiser preference
     */
    public Candidate(String inName, String inParty, String inSlogan, String inAd, String inFund)
    {
        name = inName;
        party = inParty;
        slogan = inSlogan;
        money = randomNum.nextInt(101);
        total_money += money;
        int inAdPrefer = -1, inFundPrefer = -1;
        if (inAd.equals("Issue"))
        {
            inAdPrefer = 0;
        }
        else if (inAd.equals("Attack"))
        {
            inAdPrefer = 1;
        }
        else if (inAd.equals("Hall"))
        {
            inAdPrefer = 2;
        }
        setAdPrefer(inAdPrefer);

        if (inFund.equals("Social"))
        {
            inFundPrefer = 0;
        }
        else if (inFund.equals("Phone"))
        {
            inFundPrefer = 1;
        }
        else if (inFund.equals("PAC"))
        {
            inFundPrefer = 2;
        }
        setFundPrefer(inFundPrefer);
    }

    /**
     * Copy constructor takes in a candidate and makes a deep copy of that candidate's attributes.
     * @param the candidate to be copied.
     */
    public Candidate(Candidate inCandidate)
    {
        setName(inCandidate.getName());
        setParty(inCandidate.getParty());
        setSlogan(inCandidate.getSlogan());
        money = inCandidate.getMoney();
        ad_prefer = inCandidate.getAdPrefer();
        fund_prefer = inCandidate.getFundPrefer();
    }

    /** 
     * The setName method sets the candidate's name. 
     * @param inName is the string that becomes the candidate's new name.
     */
    public void setName(String inName)
    {
        name = inName;
    }

    /**
     * getName gives access to the candidate's name.
     * @return the candidate's current name.
     */
    public String getName()
    {
        return name;
    }

    /** 
     * setSlogan sets the candidate's slogan.
     * @param inSlogan is a string that becomes the new slogan for the candidate.
     */
    public void setSlogan(String inSlogan)
    {
        slogan = inSlogan;
    }

    /** 
     * getSlogan gives access to the candidate's slogan.
     * @return the candidate's current slogan.
     */
    public String getSlogan()
    {
        return slogan;
    }

    /** 
     * setParty sets the candidate's slogan.
     * @param inParty is a string that becomes the new party for the candidate.
     */
    public void setParty(String inParty)
    {
        party = inParty;
    }

    /** 
     * getParty gives access to the candidate's party.
     * @return the candidate's current party.
     */
    public String getParty()
    {
        return party;
    }

    /**
     * setAdPrefer sets a random ad preference by selecting an integer identifier that corresponds to a specific type of ad.
     * 0 = "Issue-Based", 1 = "Attack Ad", 2 = "Town Hall"
     */
    public void setAdPrefer()
    {
        // number of ads is a variable to account for the potential of additional future subclasses.
        ad_prefer = randomNum.nextInt(number_ads);
    }

    /**
     * setAdPrefer sets an input ad preference by selecting an integer identifier that corresponds to a specific type of ad.
     * 0 = "Issue-Based", 1 = "Attack Ad", 2 = "Town Hall"
     */
    public void setAdPrefer(int inAdPrefer)
    {
        // number of ads is a variable to account for the potential of additional future subclasses.
        if (inAdPrefer < number_ads)
        {
            ad_prefer = inAdPrefer;
        }
        else
        {
            setAdPrefer();
        }
    }

    /**
     * getAdPrefer allows access to the ad preference.
     * @return the ad preference identifier
     */
    public int getAdPrefer()
    {
        return ad_prefer;
    }

    /**
     * setFundPrefer selects a random fundraiser preference by selecting an integer identifier that corresponds to a specific type of ad.
     * 0 = "Social Event", 1 = "Automated Phone Call", 2 = "Political Action Committee"
     */
    public void setFundPrefer()
    {
        // Number of fundraisers is a variable to account for the potential of additional future subclasses.
        fund_prefer = randomNum.nextInt(number_fundraisers);
    }

    /**
     * setFundPrefer selects an input fundraiser preference by selecting an integer identifier that corresponds to a specific type of ad.
     * 0 = "Social Event", 1 = "Automated Phone Call", 2 = "Political Action Committee"
     */
    public void setFundPrefer(int inFundPrefer)
    {
        // Number of fundraisers is a variable to account for the potential of additional future subclasses.
        if (inFundPrefer < number_fundraisers)
        {
            fund_prefer = inFundPrefer;
        }
        else
        {
            setFundPrefer();
        }
    }

    /**
     * getFundPrefer allows access to the fundraiser preference.
     * @return the fundraisers preference identifier
     */
    public int getFundPrefer()
    {
        return fund_prefer;
    }

    /**
     * Strategize takes in an integer of the highest money and helps the candidate determine whether they should use a new strategy for advertising and fundraising.
     * @param highest_money is the amount of money of the party or overall leader.
     */
    public void Strategize(double highest_money)
    {
        if (getMoney() < 0.1 * highest_money)
        {
            setAdPrefer();
            setFundPrefer();
        }
    }

    /**
     * setMoneyMod ads the input value to the current money modifier.
     * @param inMoneyMod is the value to add to the money modifier.
     */
    public void setMoneyMod(double inMoneyMod)
    {
        money_mod += inMoneyMod;
    }

    /**
     * setDebateMod ads the input value to the current debate modifier.
     * @param inDebateMod is the value to add to the debate modifier.
     */
    public void setDebateMod(double inDebateMod)
    {
        debate_mod += inDebateMod;
    }

    /** addMoney adds money to the candidate's total funds, also adds to the total_money total of all candidates.
     * @param add_money is the amount of money that will be added to the candidate's funds.
     */
    public void addMoney(double add_money)
    {
        money += add_money;
        total_money += add_money;
    }

    public void transferMoney(double add_money)
    {
        money += add_money;
    }

    /** getMoney gives access to the candidate's current funds.
     * @return the candidate's current sum of money.
     */
    public double getMoney()
    {
        return money;
    }

    /**
     * getTotalMoney allows access to the total money in play.
     * @return the total money in play.
     */
    public double getTotalMoney()
    {
        return total_money;
    }

    /**
     * getMoneyMod allows access to the candidate's money modifier. Returns 0 if the money modifier is less than 0.
     * @return the value of the money modifier.
     */
    public double getMoneyMod()
    {
        if (money_mod < 0)
        {
            return 0;
        }
        else
        {
            return money_mod;
        }
    }

    /**
     * getDebateMod allows access to the candidate's debate modifier. Returns 0 if the debate modifier is less than 0.
     * @return the value of the debate modifier.
     */
    public double getDebateMod()
    {
        if (debate_mod < 0)
        {
            return 0;
        }
        else
        {
            return debate_mod;
        }
    }

    /** 
     * endorsement checks the input advertisement to see if it is the candidate's prefered advertisment type.
     * @return a boolean designating whether the advertisement was of the preferred type.
     */
    public boolean endorsement(Advertisement inAdvertisement)
    {
        if (inAdvertisement.getType() == getAdPrefer())
        {
            return true;
        }
        else
        {
            return false;
        }
        
    }

    /**
     * equals compares the names of two candidates and determines if the names are equal.
     * @return A boolean stating whether the names are equal.
     */
    public boolean equals(Candidate cand2)
    {
        boolean status;
        if (getName().equals(cand2.getName()))
        {
            status = true;
        }
        else
        {
            status = false;
        }
        return status;
    }

    /**
     * compareTo compares the money of two candidates and determines if they are equal, greater than, or less than. If they are equal, they may break the tie based on names.
     * @return a integer indicating whether the candidate has more, less, or equal money.
     */

    public int compareTo(Candidate cand2)
    {
        int status;
        if (getMoney() == cand2.getMoney())
        {
            status = 0;
            if (!getName().equals(cand2.getName()))
            {
                status = getName().compareTo(cand2.getName());
            }
        }
        else if (getMoney() > cand2.getMoney())
        {
            status = 1;
        }
        else
        {
            status = -1;
        }
        return status;
    }

    /**
     * Returns a string that provides information about the candidate.
     * @return the information string
     */
    public String toString()
    {
        String ad = "";
        String fund = "";
        if (getAdPrefer() == 0)
        {
            ad = "Issue Based";
        }
        else if (getAdPrefer() == 1)
        {
            ad = "Attack Ad";
        }
        else if (getAdPrefer() == 2)
        {
            ad = "Town Hall";
        }

        if (getFundPrefer() == 0)
        {
            fund = "Social Event";
        }
        else if (getFundPrefer() == 1)
        {
            fund = "Automated Phone Call";
        }
        else if (getFundPrefer() == 2)
        {
            fund = "Political Action Committee";
        }

        return "Candidate named " + getName() + ":\n\tParty: " + getParty() + "\n\tSlogan: " + getSlogan() + "\n\tCurrent Funds: $" + getMoney() + "\n\tMoney Modifier: " + getMoneyMod() + "\n\tDebate Modifier: " + getDebateMod() + "\n\tAdvertisement Preference: " + ad + "\n\tFundraiser Preference: " + fund + "\n";
    }

}
