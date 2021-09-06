/**
 * The Message class provides methods to operate on a message string.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 6
 */

import java.io.Serializable;

public class Message implements Serializable
{
    private String message = "";

    /**
     * Parameter constructor creates a message object.
     * @param inMsg is the message to be created in the object.
     */
    public Message(String inMsg)
    {
        setMessage(inMsg);
    }

    /**
     * setMessage sets the message to the input.
     * @param inMsg is the new message.
     */
    private void setMessage(String inMsg)
    {
        message = inMsg;
    }

    /**
     * toString returns the message variable.
     * @return message variable
     */
    public String toString()
    {
        return message;
    }

    /**
     * convert finds the most and least common letters and replaces them in the string. It then appends them to the end so they can be unswapped later.
     */
    public void convert()
    {
        int max = 0;
        int min = 2;
        int counter = 0;
        char maxLetter = message.charAt(0);
        char minLetter = message.charAt(0);
        String msgCheck = message.toLowerCase();

        for (int x = 0; x < msgCheck.length(); x++)
        {
            char thisLetter = msgCheck.charAt(x);
            counter = 0;
            for (int y = 0; y < msgCheck.length(); y++)
            {
                if (msgCheck.charAt(y) == thisLetter)
                {
                    counter++;
                }
            }
            
            if (counter > max)
            {
                max = counter;
                maxLetter = thisLetter;
            }
            if (counter < min)
            {
                min = counter;
                minLetter = thisLetter;
            }
            if (counter == min)
            {
                if ((int) thisLetter < (int) minLetter)
                {
                    min = counter;
                    minLetter = thisLetter;
                }
            }
        }
        message.replace(maxLetter, minLetter);
        message.replace(minLetter, maxLetter);
        message = message + maxLetter;
        message = message + minLetter;
        
    }

    /**
     * revert undos the changes from convert, and removes the last two letters, which were just the max and min letters found in convert.
     */
    public void revert()
    {
        char minLetter = message.charAt(message.length() - 1);
        char maxLetter = message.charAt(message.length() - 2);
        message.replace(minLetter, maxLetter);
        message.replace(maxLetter, minLetter);
        message = message.substring(0, message.length() - 2);
    }

    /**
     * toMorseCode converts the message from english to morse code.
     */
    public void toMorseCode()
    {
        String morse_message = "";
        String[] morse = {" ", "--.--", ".-.-.-", "..--..", "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.", ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};
        String[] english = {" ", ",", ".", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};

        String lowerMsg = message.toLowerCase();

        for (int z = 0; z < lowerMsg.length(); z++)
        {
            for (int w = 0; w < english.length; w++)
            {
                char temp_english = english[w].charAt(0);
                if (lowerMsg.charAt(z) == temp_english)
                {
                    morse_message = morse_message + morse[w] + " ";
                }
            }
        }
        message = morse_message;
    }

    /**
     * fromMorseCode converts the message from morse code to english. All spaces are removed for some unknown reason (possibly unicode value) so testers beware.
     */
    public void fromMorseCode()
    {
        String english_message = "";
        String[] morse = {" ", "--.--", ".-.-.-", "..--..", "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.", ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};
        String[] english = {" ", ",", ".", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};

        String[] message_tokens = message.split(" ");

        for (int z = 0; z < message_tokens.length; z++)
        {
            for (int w = 0; w < morse.length; w++)
            {
                if (message_tokens[z].equals(morse[w]))
                {
                    english_message = english_message + english[w];
                }
            }
        }
        message = english_message;
    }
     
}
