/**
 * @author Lance Wilson
 * @version Lab 10
 */

public class CannibalismException extends Exception
{
     public String getMessage()
     {
          return "You attempted to have two members of the same class pounce on eachother.  That behaviour is against the rules!";
     }
}
