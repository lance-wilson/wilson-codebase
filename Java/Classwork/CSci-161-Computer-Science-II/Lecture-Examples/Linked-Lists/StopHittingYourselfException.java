public class StopHittingYourselfException extends Exception
{
     public String getMessage()
     {
          return "You attempted to have a Predator pounce on itself.  That behaviour is against the rules!";
     }
}