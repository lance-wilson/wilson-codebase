public class Team
{
    int score = 0;
    String teamName = "";

    public Team() // Default quidditch team is the 1993-94 Gryffindor Quidditch Team
    {
        setTeamName("Gryffindor Quidditch Team, 1993-94");
    }

    public Team(String inTeamName)
    {
        setTeamName(inTeamName);
    }

    public void setTeamName(String inTeamName)
    {
        teamName = inTeamName;
    }

    public String getTeamName()
    {
        return teamName;
    }

    public void addScore(int add)
    {
        score += add;
    }

    public int getScore()
    {
        return score;
    }

}
