/**
 * @author Lance Wilson
 * @version Lab 10
 */
public class DoubleTeamException extends Exception
{
     public String getMessage()
     {
          return "You attempted to have a Predator be its own partner.  That behaviour is against the rules!";
     }
}
