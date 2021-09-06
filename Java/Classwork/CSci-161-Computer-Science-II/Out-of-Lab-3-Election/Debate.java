/**
 * The Debate Class is used to simulate a debate between multiple candidates.  
 * A debate has a location, a win message, candidates, and a debate simulation.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */
import java.util.*;

public class Debate
{
    private String location = ""; //Location
    private String win_message = "";
    private ArrayList<Candidate> candidate = new ArrayList<>();
    Random randomNum = new Random();

    /**
     * Default constructor creates a debate with a default location of Okay, OK, and some default candidates.
     */
    public Debate()
    {
        setLocation("Okay, OK");
        ArrayList<Candidate> default_candidate = new ArrayList<>();
        for (int k = 0; k < randomNum.nextInt(10); k++)
        {
            default_candidate.add(new Candidate());
        }
        setCandidates(default_candidate);
    }

    /**
     * Parameter Constructor takes in a location and sets that to be the location of the debate. It also takes in an ArrayList of candidates who are going to participate in the debate.
     * @param inLocation becomes the location of the debate.
     * @param inCandidates is the ArrayList of participating candidates.
     * @exception TooLowInPollsException if candidate doesn't have enough money to participate in the debate.
     */
    public Debate(String inLocation, ArrayList<Candidate> inCandidates) throws TooLowInPollsException
    {
        setLocation(inLocation);
        setCandidates(inCandidates);
        for (int i = 0; i < inCandidates.size(); i++)
        {
            // Check if candidate has enough money.
            if (inCandidates.get(i).getMoney() < 0.03 * inCandidates.get(i).getTotalMoney())
            {
                // If not, check to see if it is the same party as the other candidates.
                /*boolean party_determine;
                for (int c = 1; c < inCandidates.size(); c++)
                {
                    party_determine = true;
                    int f = c - 1;
                    // Determines if the cth candidate's party is the same as the party of any candidate with a prior index.
                    while (f >= 0)
                    {
                        if (candidate.get(c).getParty().equals(candidate.get(f).getParty()))
                        {
                            party_determine = false;
                        }
                        f--;
                    }
                    // If the candidate's party is unique, throw too low in polls exception.
                    if (party_determine)
                    {*/
                        throw new TooLowInPollsException();
                    //}
                //}
            }
        }
    }

    /** 
     * setLocation sets the debate's location.
     * @param inLocation is a string that becomes the new location for the debate.
     */
    public void setLocation(String inLocation)
    {
        location = inLocation;
    }

    /**
     * getLocation allows access to the debate location.
     * @return the current location of the debate.
     */
    public String getLocation()
    {
        return location;
    }

    /**
     * setCandidates sets the debate's candidates. If one candidate is equal to another, that candidate is not added to the debate.
     * @param inCandidate is the ArrayList of candidates entering the debate.
     */
    public void setCandidates(ArrayList<Candidate> inCandidate)
    {
        boolean check;
        for (int i = 0; i < inCandidate.size(); i++)
        {
            check = true;
            for (int j = (i+1); j < inCandidate.size(); j++)
            {
                if (inCandidate.get(i).equals(inCandidate.get(j)))
                {
                    check = false;
                }
            }
            if (check)
            {
                candidate.add(inCandidate.get(i));
            }
        }
    }

    /**
     * getCandidates gets the names of the candidates.
     * @return String of all candidate names.
     */
    public String getCandidates()
    {
        String cand_names = "";
        for (int aaa = 0; aaa < candidate.size() - 1; aaa++)
        {
            cand_names = cand_names + "\t" + candidate.get(aaa).getName() + "\n"; 
        }
        cand_names = cand_names + "\t" + candidate.get(candidate.size() - 1).getName() + "\n";
        return cand_names;
    }

    /**
     * getCandidate allows access to the ArrayList of candidates.
     * @return the ArrayList of candidates.
     */
    public ArrayList<Candidate> getCandidate()
    {
        return candidate;
    }

    /**
     * debate_act is the simulation of the debate.  It generates random numbers for each candidate, and declares the winner to be the candidate with the largest number. Money changes hands by the formula candidate's money * (debate_score_total - candidate's debate_score)/debate_score_total.
     * @return the string of whether the message about who won the debate.
     */
    public String debate_act()
    {
        if (getCandidate().size() == 0)
        {
            return "No candidate is high enough in the polls.";
        }
        double[] debate_score = new double[getCandidate().size()];
        double debate_score_total = 0;

        for (int y = 0; y < candidate.size(); y++)
        {
            debate_score[y] = randomNum.nextInt(101)*getCandidate().get(y).getDebateMod();
            debate_score_total += debate_score[y];
        }

        double highest = debate_score[0];
        int win_number = 0;
        // Find highest debate score by sequential search
        for (int m = 1; m < getCandidate().size(); m++)
        {
            if (debate_score[m] > highest)
            {
                highest = debate_score[m];
                win_number = m;
            }
            // Tiebreaker
            if (debate_score[m] == highest)
            {
                int tiebreaker1 = randomNum.nextInt(101);
                int tiebreaker2 = randomNum.nextInt(101);
                if (tiebreaker1 < tiebreaker2)
                {
                    highest = debate_score[m];
                    win_number = m;
                }
            }
        } // End for loop

        win_message = getCandidate().get(win_number).getName() + " won the debate and collected money as follows:\n";

        double winnings = 0;
        if (win_number != 0)
        {
            for (int n = 0; n < win_number; n++)
            {
                //winnings = getCandidate().get(n).getMoney() * (debate_score_total - debate_score[n])/debate_score_total;
                winnings = getCandidate().get(n).getMoney() * (debate_score_total - debate_score[win_number] - debate_score[n])/(30.0 *(debate_score_total + debate_score[win_number] + debate_score[n]));
                win_message = win_message + "\tFrom " + getCandidate().get(n).getName() + ": $" + winnings + "\n";
                getCandidate().get(win_number).addMoney(winnings);
                getCandidate().get(n).addMoney(-1 * winnings);
            }
        }
        for (int p = (win_number+1); p < candidate.size(); p++)
        {
            //winnings = getCandidate().get(p).getMoney() * (debate_score_total - debate_score[p])/debate_score_total;
            winnings = getCandidate().get(p).getMoney() * (debate_score_total - debate_score[win_number] - debate_score[p])/(30.0*(debate_score_total + debate_score[win_number] + debate_score[p]));
            win_message = win_message + "\tFrom " + getCandidate().get(p).getName() + ": $" + winnings + "\n";
            getCandidate().get(win_number).addMoney(winnings);
            getCandidate().get(p).addMoney(-1 * winnings);
        }

        return win_message;

    }

    /**
     * Returns a string that provides information about the debate.
     * @return the information string
     */
    public String toString()
    {
        return "Debate at Location: " + getLocation() + "\nwith candidates: \n" + getCandidates() + "had the following result:\n\n" + win_message;
    }

}
