/**
 * The Driver Class is used to simulate an election.  
 * The Driver uses the Advertisement, Candidate, Debate, Election, and Fundraiser classes, as well as the PACFUndraiser, SocialFundraiser, PhoneFundraiser, TownHallAdvertisement, IssueBasedAdertisement, and AttackBasedAdvertisement classes, which it uses to simulate various events leading up to an election, and then simulates the election itself.  
 * <br><br>
 * @author Lance Wilson
 * @version OoL #3
 */
import java.util.*;
import java.io.*;

public class Driver
{
    public static void main(String[] args)
    {
        // Define variables
        String debateWinner = "";
        String electionWinner = "";
        String debate_result;
        int i, k, r, j, jj, kk;
        int add_money;

        /*int best_Ad = 0;
        int best_fund = 2;
        int worst_Ad = 2;
        int worst_fund = 1;*/

        // Uncomment for user inputted filename.
        //Scanner cmdLine = new Scanner(System.in);
        //System.out.println("Please enter the filename of candidates:");
        //String filename = cmdLine.nextLine();
        Random randomNum = new Random();

        // Create an array of candidates.
        ArrayList<Candidate> candidate = new ArrayList<Candidate>();
        ArrayList<String> parties = new ArrayList<String>();
        ArrayList<String> location = new ArrayList<String>();
        // Create file scanners
        Scanner candFile = new Scanner(System.in);
        Scanner locFile = new Scanner(System.in);

        try
        {
            // Open files and set the scanners to use those files.
            File candidateFile = new File("CandidateManyMany.txt");
            candFile = new Scanner(candidateFile);
            File locationFile = new File("Locations.txt");
            locFile = new Scanner(locationFile);
        }
        catch (FileNotFoundException e)
        {
            System.err.println(e.getMessage());
            System.exit(1);
        }


        // While there are still candidates in the file, read the next line, separate on a delimiter of "1", and then send the three tokens of data to a parameter constructor to create a new candidate, and add that candidate to the candidate ArrayList.
        int g = 0;
        while (candFile.hasNext())
        {
            String line = candFile.nextLine();
            String[] tokens = line.split("1");
            candidate.add(new Candidate(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]));
            boolean match = false;
            for (String party : parties)
            {
                if(party.equals(tokens[1]))
                {
                     match = true;
                }
            }
            if (!match)
            {
                parties.add(tokens[1]);
            }
            g++;
        }
        // Close file
        candFile.close();
        ArrayList<ArrayList<Candidate>> candList = new ArrayList<ArrayList<Candidate>>();
        ArrayList<String> previous_party = new ArrayList<String>();
        candList = ListOfLists(candidate, parties, candList, previous_party);

        /*for (int gamma = 0; gamma < candList.size(); gamma++)
        {
            for (int delta = 0; delta < candList.get(gamma).size(); delta++)
            {
                System.out.println(candList.get(gamma).get(delta).getName() + " " + candList.get(gamma).get(delta).getMoney());
            }
            System.out.println("\nEnd of " + parties.get(gamma) + " party\n");
        }*/

        r = 0;
        // While there is still data left in the location file, read the next line and add it to the location ArrayList.
        while (locFile.hasNext())
        {
            String line = locFile.nextLine();
            location.add(line);
            r++;
        }
        // Close file
        locFile.close();

        // Loop runs through 365 days.
        for (i = 0; i < 365; i++)
        {
System.out.println("Day " + i);
            /*if (i == 153)
            {
                for (int omicron = 0; omicron < candList.size(); omicron++)
                {
                    for (int rho = 0; rho < candList.get(omicron).size(); rho++)
                    {
                        boolean just_modded = false;
                        if (candList.get(omicron).get(rho).getAdPrefer() == best_Ad && candList.get(omicron).get(rho).getFundPrefer() == best_fund)
                        {
                            candList.get(omicron).get(rho).setAdPrefer(worst_Ad);
                            candList.get(omicron).get(rho).setFundPrefer(worst_fund);
                            just_modded = true;
                        }
                        if (candList.get(omicron).get(rho).getAdPrefer() == worst_Ad && candList.get(omicron).get(rho).getFundPrefer() == worst_fund && !just_modded)
                        {
                            candList.get(omicron).get(rho).setAdPrefer(best_Ad);
                            candList.get(omicron).get(rho).setFundPrefer(best_fund);
                        }
                    }
                }
            } // End halfway strategy switch*/

            if (i == 306)
            {
                // Transfer funds to top candidate in each party
                // Remove all but top candidate in each party
                for (int n = 0; n < candList.size(); n++)
                {
                    int best = candList.get(n).size() - 1;
                    for (int o = 0; o < best; o++)
                    {
                        candList.get(n).get(best).transferMoney(candList.get(n).get(o).getMoney());
                    }
                    Candidate best_cand = candList.get(n).get(best);
                    candList.get(n).clear();
                    candList.get(n).add(best_cand);
                    candList.get(n).get(0).setAdPrefer(0);
                    candList.get(n).get(0).setFundPrefer(2);
                    if (candList.get(n).get(0).getMoneyMod() < 1.0)
                    {
                        candList.get(n).get(0).setMoneyMod(25.0);
                    }
                    candList.get(n).get(0).setDebateMod(1.0 - candList.get(n).get(0).getDebateMod());
                }
            } // End day 306 jettison

            // For loop executes for each candidate.
            for (j = 0; j < candList.size(); j++)
            {
                for (jj = 0; jj < candList.get(j).size(); jj++)
                {
                    // Calculate weighting value
                    int weight = randomNum.nextInt(10);

                    if (parties.size() > 2)
                    {
                        if (!candList.get(j).get(jj).getParty().equals(parties.get(0)) && !candList.get(j).get(jj).getParty().equals(parties.get(1)))
                        {
                            weight = 9;
                        }
                    }

                    if (i < 250)
                    {
                        // 30% of the time before day 250, candidate holds a fundraiser.
                        if (weight < 3)
                        {
                            fundraise_attempt(candList.get(j).get(jj), location.get(randomNum.nextInt(location.size())));
                        }
                        // 70% of the time before day 250, candidate runs an advertisement.
                        else
                        {
                            k = randomNum.nextInt(candList.size());
                            kk = randomNum.nextInt(candList.get(k).size());
                            // Make sure that the potential target candidate is not the candidate.
                            while (jj == kk && j == k)
                            {
                                k = randomNum.nextInt(candList.size());
                                kk = randomNum.nextInt(candList.get(k).size());
                            }
                            advertise_attempt(candList.get(j).get(jj), candList.get(k).get(kk), location.get(randomNum.nextInt(location.size())));
                        }
                    }
                    else  // After day 250.
                    {
                        // Fundraiser occurs 60% of the time.
                        if (weight < 6)
                        {
                            fundraise_attempt(candList.get(j).get(jj), location.get(randomNum.nextInt(location.size())));
                        }
                        // Advertisement occurs 40% of the time.
                        else
                        {
                            k = randomNum.nextInt(candList.size());
                            kk = randomNum.nextInt(candList.get(k).size());
                            // Make sure that the potential target candidate is not the candidate.
                            while (jj == kk && j == k)
                            {
                                k = randomNum.nextInt(candList.size());
                                kk = randomNum.nextInt(candList.get(k).size());
                            }
                            advertise_attempt(candList.get(j).get(jj), candList.get(k).get(kk), location.get(randomNum.nextInt(location.size())));
                        }
                    }
                }
            } // End for loop for each candidate's action

            // ArrayList for candidates for the debate.
            ArrayList<Candidate> debate_candidates = new ArrayList<Candidate>();
            // Occurs on days divisible by 10 before day 305.
            if (i % 10 == 0) // && i < 305
            {
                for (int epsilon = 0; epsilon < candList.size(); epsilon++)
                {
                    for (int zeta = 0; zeta < candList.get(epsilon).size(); zeta++)
                    {
                        debate_candidates.add(candList.get(epsilon).get(zeta));
                    }
                }
                boolean done = false;
                while (!done && debate_candidates.size() != 0)
                {
                    try
                    {
                        Debate debate = new Debate(location.get(randomNum.nextInt(location.size())), debate_candidates);
                        debate_result = "";
                        debate_result = debate.debate_act();
                        System.out.println(debate);
                        done = true;
                    }
                    catch (TooLowInPollsException e)
                    {
                        System.err.println(e.getMessage() + "\nRemoving lowest candidate.");
                        Candidate low = debate_candidates.get(0);
                        for (int c = 1; c < debate_candidates.size(); c++)
                        {
                           if (low.getMoney() > debate_candidates.get(c).getMoney())
                           {
                                low = debate_candidates.get(c);
                           }
                        }
                        debate_candidates.remove(low);
                    }
                }
            }

            if (i <= 305)
            {
                // Redistribute money if anyone has more than max primary money
                // Block for redistribution of all parties
                /*for (int upsilon = 0; upsilon < candList.size(); upsilon++)
                {
                    Collections.sort(candList.get(upsilon));

                    if (candList.get(upsilon).size() >= 2)
                    {
                        double free_float = (candList.get(upsilon).get(candList.get(upsilon).size()-1).getMoney() - candList.get(upsilon).get(candList.get(upsilon).size()-2).getMoney()) * 0.8;
                        for (int omega = 0; omega < (candList.get(upsilon).size()-1); omega++)
                        {
                            //int index = candList.get(upsilon).size() - omega;
                            double index = (double) omega + 1.0;
                            double distributed_money = free_float * 9.0 / (Math.pow(10.0, index));
                            candList.get(upsilon).get(omega).transferMoney(distributed_money);
                            candList.get(upsilon).get(candList.get(upsilon).size()-1).transferMoney(-1*distributed_money);
                        }
                    }
                }*/

                //Block for redistribution of just one party
                Collections.sort(candList.get(1));

                double free_float = (candList.get(1).get(candList.get(1).size()-1).getMoney() - candList.get(1).get(candList.get(1).size()-2).getMoney()) * 0.8;

                for (int omega = 0; omega < (candList.get(1).size()-1); omega++)
                {
                    double index = (double) omega + 1.0;
                    double distributed_money = free_float * 9.0 / (Math.pow(10.0, index));
                    candList.get(1).get(omega).transferMoney(distributed_money);
                    candList.get(1).get(candList.get(1).size()-1).transferMoney(-1*distributed_money);
                }

                // Make primaries less close
                Collections.sort(candList.get(0));
                for (int ww = 0; ww < (candList.get(0).size() - 2); ww++)
                {
                    double distributed_money = (candList.get(0).get(ww).getMoney() * 0.2);
                    candList.get(0).get(candList.get(0).size() - 1).transferMoney(distributed_money);
                    candList.get(0).get(ww).transferMoney(-1 * distributed_money);
                }


                // Sort each party's list
                for (int mu = 0; mu < candList.size(); mu++)
                {
                    Collections.sort(candList.get(mu));
                }
                // Print out candidates
                for (int gamma = 0; gamma < candList.size(); gamma++)
                {
                    for (int delta = 0; delta < candList.get(gamma).size(); delta++)
                    {
                        System.out.println(candList.get(gamma).get(delta));
                    }
                }

                double[] second_percent = new double[candList.size()];
                double[] third_percent = new double[candList.size()];

                System.out.println("-----------PRIMARY RESULTS-----------");

                // Calculate how much money the second and third place candidates have as a percentage of the leading candidate's money
                for (int rr = 0; rr < candList.size(); rr++)
                {
                    if (candList.get(rr).size() >= 2)
                    {
                        second_percent[rr] = (candList.get(rr).get(candList.get(rr).size() - 2).getMoney()/candList.get(rr).get(candList.get(rr).size() - 1).getMoney()) * 100.0;
                        System.out.println(candList.get(rr).get(0).getParty() + " Second: " + second_percent[rr]);        
                        if (candList.get(rr).size() >= 3)
                        {                
                            third_percent[rr] = (candList.get(rr).get(candList.get(rr).size() - 3).getMoney()/candList.get(rr).get(candList.get(rr).size() - 1).getMoney()) * 100.0;
                            System.out.println(candList.get(rr).get(0).getParty() + " Third: " + third_percent[rr]);
                        }
                        System.out.println();
                    }
                }

            }

            ArrayList<Candidate> candPostPrimary = new ArrayList<Candidate>();
            if (i > 305)
            {
                // Create a list of post-primary candidates
                for (int nu = 0; nu < candList.size(); nu++)
                {
                    candPostPrimary.add(candList.get(nu).get(0));
                }
                // Sort the new list
                Collections.sort(candPostPrimary);
                // Print the candidates
                for (int sigma = 0; sigma < candPostPrimary.size(); sigma++)
                {
                    System.out.println(candPostPrimary.get(sigma));
                }

                // Calculate the results of each candidate as a percentage of the leading candidate's money.
                System.out.println("-----------POST-PRIMARY RESULTS-----------");
                for (int qq = (candPostPrimary.size() - 2); qq >= 0; qq--)
                {
                    double percent = (candPostPrimary.get(qq).getMoney()/candPostPrimary.get(candPostPrimary.size()-1).getMoney()) * 100.0;
                    int place = candPostPrimary.size() - qq;
                    System.out.println(place + " Place: " + percent);
                }

                
            }


            // Strategizing block
            /*if (i <= 305)
            {
                double highest_money = 0;
                for (int tau = 0; tau < candList.size(); tau++)
                {
                    highest_money = candList.get(tau).get(0).getMoney();
                    // Find highest value of money
                    for (int eta = 1; eta < candList.get(tau).size(); eta++)
                    {
                        if (candList.get(tau).get(eta).getMoney() > highest_money)
                        {
                            highest_money = candList.get(tau).get(eta).getMoney();
                        }
                    }
                    // Have each candidate strategize based on the value of highest money
                    for (int iota = 0; iota < candList.get(tau).size(); iota++)
                    {
                        candList.get(tau).get(iota).Strategize(highest_money);
                    }
                }
            }
            if (i > 305)
            {
                double highest_money = candList.get(0).get(0).getMoney();
                for (int kappa = 1; kappa < candList.size(); kappa++)
                {
                    if (candList.get(kappa).get(0).getMoney() > highest_money)
                    {
                        highest_money = candList.get(kappa).get(0).getMoney();
                    }
                }
                for (int lambda = 0; lambda < candList.size(); lambda++)
                {
                    candList.get(lambda).get(0).Strategize(highest_money);
                }
            }*/

        } // End of 365 Day loop.

        //Election
        ArrayList<Candidate> electionList = new ArrayList<Candidate>();
        for (k = 0; k < candList.size(); k++)
        {
            for (kk = 0; kk < candList.get(k).size(); kk++)
            {
                electionList.add(candList.get(k).get(kk));
            }
        }
        Election election = new Election(electionList);
        election.election_vote();
        System.out.println(election);

    } //End Main method

    public static void fundraise_attempt(Candidate candidate, String location)
    {
        Random randomNum = new Random();
        try
        {
            //Create prefered fundraiser
            if (candidate.getFundPrefer() == 0)
            {
                SocialFundraiser social = new SocialFundraiser(candidate, location);
                social.changeMods();
                System.out.println(social);
            }
            else if (candidate.getFundPrefer() == 1)
            {
                PhoneFundraiser phoneCall = new PhoneFundraiser(candidate, location);
                phoneCall.changeMods();
                System.out.println(phoneCall);
            }
            else
            {
                PACFundraiser pac = new PACFundraiser(candidate, location);
                pac.changeMods();
                System.out.println(pac);
            }
        }
        catch (TooLowInPollsException e)
        {
            System.err.println(e.getMessage() + "\n\tAction: PAC Fundraiser");
            //Random non-PAC Fundraiser
            if (randomNum.nextInt(2) == 0)
            {
                SocialFundraiser social = new SocialFundraiser(candidate, location);
                social.changeMods();
                System.out.println(social);
            }
            else
            {
                PhoneFundraiser phoneCall = new PhoneFundraiser(candidate, location);
                phoneCall.changeMods();
                System.out.println(phoneCall);
            }
        }
    }

    public static void advertise_attempt(Candidate candidate, Candidate candidate2, String location)
    {
        Random randomNum = new Random();
        String advertise_string;
        try
        {
            //Create random advertisement
            int aa = randomNum.nextInt(3);
            if (aa == 0)
            {
                IssueBasedAdvertisement issue = new IssueBasedAdvertisement(candidate);
                advertise_string = issue.approval();
                System.out.println(issue);
            }
            else if (aa == 1)
            {
                AttackAdvertisement attack = new AttackAdvertisement(candidate, candidate2);
                advertise_string = attack.approval();
                System.out.println(attack);
            }
            else
            {
                TownHallAdvertisement town_hall = new TownHallAdvertisement(candidate);
                advertise_string = town_hall.approval();
                System.out.println(town_hall);
            }
        }
        catch (OutOfMoneyException e)
        {
            //Fundraiser instead
            System.err.println("Candidate cannot afford an advertisement, so will attempt a fundraiser instead.");
            fundraise_attempt(candidate, location);
        }
    }

    // party_number must be declared outside ListOfLists so the value stays constant for all runs of the method.
    static int party_number = -1;

    public static ArrayList<ArrayList<Candidate>> ListOfLists(ArrayList<Candidate> candidate, ArrayList<String> party, ArrayList<ArrayList<Candidate>> candList, ArrayList<String> previous_party)
    {
        // Base case where there is only 1 candidate.
        if (candidate.size() == 1)
        {
            // Loop through all parties to decide which ArrayList of candidates to add to
            for (int w = 0; w < party.size(); w++)
            {
                // If this is a new party we haven't used before
                if (w >= previous_party.size())
                {
                    // Add to the previous party list
                    previous_party.add(party.get(w));
                    // Add a new List to candList
                    candList.add(new ArrayList<Candidate>());
                }
                // Double check that the candidate really is from this party
                if (candidate.get(0).getParty().equals(party.get(w)))
                {
                    // Add the candidate to the appropriate list
                    candList.get(w).add(candidate.get(0));
                }
                // Sort the candidates in that party.
                InsertionSort(candList.get(w));
            }
            return candList;
        }
        else
        {
            // Party of current candidate
            String current_party = candidate.get(0).getParty();
            int party_add = -1;
            boolean seen_before = false;
            // Check all of the previous parties to see if we have encountered this one 
            for (int c = 0; c < previous_party.size(); c++)
            {
                // previous_party mirrors the party division of the List of Lists, so party_add will represent the list that the candidate should be added to
                if (previous_party.get(c).equals(current_party))
                {
                    // If we get here, we have seen the party before, so we can just set the index of the party we want to add the candidate to
                    seen_before = true;
                    party_add = c;
                }
            }
            // Check through all parties, in case we haven't seen this one before
            for (int a = 0; a < party.size(); a++)
            {
                if (party.get(a).equals(current_party) && !seen_before)
                {
                    // If we get here, we have not seen the party before, so we need to increase the number of existing parties, add the party to the list of previous parties, and set the index of the party we want to add the candidate to.
                    party_number++;
                    seen_before = true;
                    previous_party.add(current_party);
                    party_add = a;
                }
            }

            // If there aren't enough parties in candList, add a new ArrayList
            if (candList.size() <= party_number)
            {
                candList.add(new ArrayList<Candidate>());
            }

            // Add the current candidate to the appropriate party in candList
            candList.get(party_add).add(candidate.get(0));
            // Sort that particular party's list
            InsertionSort(candList.get(party_add));
            // Remove the current candidate from the original candidate list
            candidate.remove(candidate.get(0));

            return ListOfLists(candidate, party, candList, previous_party);

        }
    }

    public static void InsertionSort(ArrayList<Candidate> candList)
    {
        Candidate unsorted = null;
        int scan;

        // Loop through ArrayList
        for (int index = 1; index < candList.size(); index++)
        {
            unsorted = candList.get(index);
            scan = index;

            // While the unsorted candidate is greater than the previous candidate, swap them
            while (scan > 0 && candList.get(scan - 1).compareTo(unsorted) == 1)
            {
                Collections.swap(candList, (scan - 1), scan);
                scan--;
            }
        }
    }

}
