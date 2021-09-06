/**
 * The Mouse Class is used to simulate a mouse.  
 * A Mouse has a name and an evasion rating.  
 * The evasion rating denotes how good the mouse is at escaping cat pounces
 * <br><br>
 * @author Scott Kerlin
 * @version Lecture 
 */
import java.util.*;
public class Mouse extends Animal implements Prey
{

     private int evasion = 0;   //Evasion rating
     private ArrayList<Mouse> mousePups = new ArrayList<Mouse>();
     
     public void addMousePup(Mouse newMousePup)
     {
          mousePups.add(newMousePup);
     }
     
     public void addMousePups(ArrayList<Mouse> litter)
     {
          for (Mouse mousePup : litter)
          {
               mousePups.add(mousePup);
          }
     }
     
     public ArrayList<Mouse> getMousePups()
     {
          return mousePups;
     }
     

     
     public String toString()
     {
          String output = "This mouse is named " + getName() + " and it has these values:\n\tEvasion: " + getEvasion() + "\n\tTag Number: " + getTag() + "\n";
          
          if (mousePups.size() == 0)
          {
               output = output + "An No MousePups!!!\n";
          }
          else
          {
               output = output + "And has these mousePups:\n-----------------\n";
               for (Mouse mousePup : mousePups)
               {
                    output = output + mousePup + "\n\n";
               }
               output = output + "\n-----------------\n";  
          }
          
          
          
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
          for (Mouse mousePup : inMouse.getMousePups())
          {
               mousePups.add(new Mouse(mousePup));
          }
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
