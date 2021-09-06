/**
 * The Mouse Class is used to simulate a mouse.  
 * A Mouse has a name and an evasion rating.  
 * The evasion rating denotes how good the mouse is at escaping cat pounces
 * <br><br>
 * @author Lance Wilson
 * @version Lab 8
 */
import java.util.*;
public class Mouse extends Animal implements Prey
{

     private int evasion = 0;   //Evasion rating

     /**
     * compareTo runs the compareTo method on the mouse's names
     * @param the other mouse
     * @return int whether the name is greater, less than, or equal to
     */
     public int compareTo(Mouse otherMouse)
     {
          return getName().compareTo(otherMouse.getName());
     }
     
    /**
     * equals determines if another mouse is equal to this mouse based on ID
     * @param the other mouse
     * @return boolean whether they are equal
     */
     public boolean equals(Mouse otherMouse)
     {
          if (getTag() == otherMouse.getTag())
          {
               return true;
          }
          return false;
     }
     
    /**
     * returns string of info about the mouse
     * @return info string
     */
     public String toString()
     {
          String output = "This cat is named " + getName() + " and it has these values:\n\tEvasion: " + getEvasion() + "\n\tTag Number: " + getTag() + "\n";

          return output;
     }
     
   
     /**
      * Default Constructor to build a Mouse with Randomly generated Evasion Rating
      */
     public Mouse()
     {
          setName("DEFAULT");
          setEvasion(rand.nextInt(11));
          setTag();
     }
     
     /**
      * Full Parameter Constructor to build a Mouse using the inputed parameter values provided
      * @param inName will be used as the Mouse's Name
      * @param inEvade will be used as the Mouse's Evasion, if it passes the validity check
      */
     public Mouse(String inName, int inEvade)
     {
          setName(inName);
          setEvasion(inEvade);
          setTag();
     }
     
     /**
      * Copy Constructor to build a Duplicate of the inputted Mouse
      * @param inMouse is the Mouse to be copied by this Mouse
      */
     public Mouse(Mouse inMouse)
     {
          setName(inMouse.getName());
          setEvasion(inMouse.getEvasion());
          setTag();
     }
     
     

     /**
      * setEvasion updates the Mouse's evasion rating
      * @param inEvade is the value which will become the Mouse's new evasion rating
      */
     public void setEvasion(int inEvade)
     {
          if (inEvade >= 0 && inEvade <= 10)
          {
               evasion = inEvade;
          }
          else
          {
               System.out.println("Invalid Rating Entered!");
          }

     }
     
     
     /**
      * getEvasion allows access to the Mouse's evasion rating
      * @return the Mouse's current evastion rating
      */
     public int getEvasion()
     {
          return evasion;
     }
     
}
