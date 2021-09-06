/**
 * The Driver class provides code to test saving message objects to a file and reading message objects from a file.
 * Requires use of the Message class.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 6
 */

import java.util.*;
import java.io.*;

public class Driver
{
    public static void main(String[] args)
    {
        String input = "";
        Scanner userIn = new Scanner(System.in);

        System.out.println("Enter \"Read\" to Read in Messages or \"Save\" to Save messages.");
        input = userIn.nextLine();

        // If reading from a file
        if (input.equalsIgnoreCase("read"))
        {
            try
            {
                // File name is entered by user, and an Object Input Stream is created.
                System.out.println("Enter the file name of the Message file.");
                String filename = userIn.nextLine();
                FileInputStream inFileStream = new FileInputStream(filename);
                ObjectInputStream inObjectStream = new ObjectInputStream(inFileStream);
                // Loop runs until exception is thrown.
                while(true)
                {
                    Message thisMsg = (Message) inObjectStream.readObject();
                    System.out.println(thisMsg);
                    thisMsg.fromMorseCode();
                    System.out.println(thisMsg);
                    thisMsg.revert();
                    System.out.println(thisMsg);
                }
            }
            catch (ClassNotFoundException e)
            {
                System.err.println(e.getMessage());
            }
            catch (IOException e)
            {
                System.out.println("End of file reached.");
            }
        }
        // Saving messages to a file
        else if (input.equalsIgnoreCase("save"))
        {
            try
            {
                // Create Object Output Stream
                FileOutputStream outStream = new FileOutputStream("Messages.dat");
                ObjectOutputStream outObject = new ObjectOutputStream(outStream);
                ArrayList<Message> saveMsg = new ArrayList<Message>();
                String check = "yes";
                // Runs while user continues to enter "yes".
                while (check.equalsIgnoreCase("yes"))
                {
                    System.out.println("Please Enter a Message.");
                    Message message = new Message(userIn.nextLine());
                    message.convert();
                    message.toMorseCode();
                    saveMsg.add(message);
                    System.out.println("Would you like to enter another message? yes or no");
                    check = userIn.nextLine();
                }
                // Write objects to file
                for (int m = 0; m < saveMsg.size(); m++)
                {
                    outObject.writeObject(saveMsg.get(m));
                }
            }
            catch (IOException e)
            {
                System.err.println("Error writing to file.");
            }
        }
        
    }
}
