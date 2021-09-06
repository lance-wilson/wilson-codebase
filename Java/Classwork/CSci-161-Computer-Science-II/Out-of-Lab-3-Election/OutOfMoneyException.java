public class OutOfMoneyException extends Exception
{
    public String getMessage()
    {
        return "This candidate does not have enough money to purchase an advertisement.";
    }

}
