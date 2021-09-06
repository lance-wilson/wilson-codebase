/**
 * The HardDriver class takes in two input integers, and, if the numbers are not negative, uses recursion to perform the ackermann function on those two numbers (assuming they are small enough to avoid an overflow error.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 7
 */
import java.util.*;

public class HardDriver
{
    public static void main(String[] args)
    {
        int input1 = 0;
        int input2 = 0;
        int result = 0;
        Scanner keyboard = new Scanner(System.in);

        while (input1 >= 0 && input2 >= 0)
        {
            System.out.println("Please enter the first number (negative number to quit):");
            input1 = keyboard.nextInt();
            keyboard.nextLine();
            System.out.println("Please enter the second number (negative number to quit):");
            input2 = keyboard.nextInt();
            if (input1 < 0 || input2 < 0)
            {
                // Exit if either input is negative.
                System.exit(0);
            }
            else
            {
                // Otherwise find ackermann function result.
                result = ackermann(input1, input2);
                // Print result
                System.out.println("Result: " + result);
            }
        }
    }

    /**
     * ackermann uses recursion to calculate the ackermann function of the inputs m and n.
     * @param m is the first input number
     * @param n is the second input number
     * @return n+1 if m is 0, ackermann function of m-1 and 1 if n is 0, and the ackermann function of m-1 and the ackermann function of m and n-1 if m and n are not 0.
     */
    public static int ackermann(int m, int n)
    {
        if (m == 0)
        {
            return n + 1;
        }
        if (n == 0)
        {
            return ackermann(m-1, 1);
        }
        else
        {
            return ackermann(m-1, ackermann(m, n-1));
        }
    }
}
