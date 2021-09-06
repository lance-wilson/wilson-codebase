/**
 * The Election Class is used to simulate the election among all the candidates.  
 * An election has a title, a winner, a result, and a vote.
 * <br><br>
 * @author Lance Wilson
 * @version OoL #2
 */
import java.util.*;

public class Election
{
    private String title = "";
    private String winner = "";
    private String result = "";
    private ArrayList<Candidate> candidate = new ArrayList<>();

    /**
     * Default constructor creates an election with a default title and default candidates.
     */
    public Election()
    {
        setTitle("US President");
        ArrayList<Candidate> default_candidate = new ArrayList<>();
        default_candidate.add(new Candidate());
        setCandidates(default_candidate);
    }

    /**
     * Parameter constructor creates an election with the inputted ArrayList for candidates and a default title.
     */
    public Election(ArrayList<Candidate> inCandidates)
    {
        setTitle("US President");
        setCandidates(inCandidates);
    }

    /**
     * Parameter constructor creates an election with the inputted string as a title and the inputted ArrayList as candidates.
     */
    public Election(String inTitle, ArrayList<Candidate> inCandidates)
    {
        setTitle(inTitle);
        setCandidates(inCandidates);
    }

    /**
     * setTitle sets the election's title.
     * @param inTitle is a string that becomes the new title for the election.
     */
    public void setTitle(String inTitle)
    {
        title = inTitle;
    }

    /**
     * getTitle allows access to the election's title.
     * @return title returns the title of the election.
     */
    public String getTitle()
    {
        return title;
    }

    /**
     * setWinner sets the winner of the election to the inputted value.
     * @param inWinner becomes the winner of the election.
     */
    public void setWinner(String inWinner)
    {
        winner = inWinner;
    }

    /**
     * getWinner allows access to the election winner.
     * @return the winner of the election.
     */
    public String getWinner()
    {
        return winner;
    }

    /**
     * setCandidates sets the election's candidates.
     * @param inCandidate is the ArrayList of candidates entering the election.
     */
    public void setCandidates(ArrayList<Candidate> inCandidate)
    {
        for (int x = 0; x < inCandidate.size(); x++)
        {
            candidate.add(inCandidate.get(x));
        }
    }

    /**
     * getCandidates gets the names of the candidates.
     * @return String of all candidate names.
     */
    public String getCandidates()
    {
        String output = "";
        for (int x = 0; x < candidate.size() - 1; x++)
        {
            output = output + candidate.get(x).getName() + ", ";
        }
        output = output + candidate.get(candidate.size()).getName();
        return output;
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
     * election_vote simulates the election by determining which candidate has the most money, and declaring that candidate the winner. If there is a tie the winner is chosen randomly.
     * @param candidate is the array of candidates involved with the election.
     * @return election_winner is the name of the winner of the election.
     */
    public String election_vote()
    {
        Random randomNum = new Random();
        double highest = getCandidate().get(0).getMoney();
        int m, win_number = 0;

        // Sequential search to find candidate with most money.
        for (m = 1; m < candidate.size(); m++)
        {
            if (getCandidate().get(m).getMoney() > highest)
            {
                highest = getCandidate().get(m).getMoney();
                win_number = m;
            }
            // Tiebreaker
            if (getCandidate().get(m).getMoney() == highest)
            {
                int tiebreaker1 = randomNum.nextInt(101);
                int tiebreaker2 = randomNum.nextInt(101);
                if (tiebreaker1 < tiebreaker2)
                {
                    highest = getCandidate().get(m).getMoney();
                    win_number = m;
                }
            }
        }

        // Set winner and create result string.
        setWinner(getCandidate().get(win_number).getName());
        result = getWinner() + " is the winner of the " + getTitle() + " election!";

        return result;  
    }

    /**
     * Returns a string that provides information about the election.
     * @return the information string
     */
    public String toString()
    {
        return result;
    }

}
