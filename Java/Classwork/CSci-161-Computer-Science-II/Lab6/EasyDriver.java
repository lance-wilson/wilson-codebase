/**
 * The EasyDriver class takes in an input integer, and, if the input is not 0, uses a recursive function to find the sum of that number and all positive numbers below it.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 7
 */
import java.util.*;

public class EasyDriver
{
    public static void main(String[] args)
    {
        int input = -1;
        int result = -1;
        Scanner keyboard = new Scanner(System.in);

        while (input != 0)
        {
            System.out.println("Please enter a number (Enter 0 to quit):");
            input = keyboard.nextInt();
            if (input == 0)
            {
                // Exit if input is 0.
                System.exit(0);
            }
            else
            {
                // Find the sum.
                result = rSum(input);
                // Print result.
                System.out.println("Result: " + result);
            }
        }
    }

    /**
     * rSum uses recursion to calculate the sum of the integer x and all positive numbers below x.
     * @param x is the input number
     * @return 0 if x is less than 1 and x + the return of the rSum function for x-1.
     */
    public static int rSum(int x)
    {
        if (x < 1)
        {
            return 0;
        }
        else
        {
            return x + rSum(x-1);
        }

    }

}
