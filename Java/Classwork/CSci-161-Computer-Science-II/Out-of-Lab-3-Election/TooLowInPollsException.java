public class TooLowInPollsException extends Exception
{
    public String getMessage()
    {
        return "This candidate does not have enough money to participate in this action.";
    }

}
