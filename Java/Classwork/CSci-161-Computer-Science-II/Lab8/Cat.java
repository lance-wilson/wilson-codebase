/**
 * The Cat Class is used to simulate a mouse.  
 * A Cat has a name, an evasion rating and a pounce rating.  
 * The evasion rating denotes how good the cat is at escaping dog pounces
 * The pounce rating denotes how good the cat is at pouncing on mice
 * <br><br>
 * @author Lance Wilson
 * @version Lab 8
 */
import java.util.*;
public class Cat extends Animal implements Predator, Prey
{

     private int evasion = 0;   //Evasion rating of Cat
     private int pounce = 0;    //Pounce rating of Cat


     /**
     * compareTo runs the compareTo method on the cat's names
     * @param the other cat
     * @return int whether the name is greater, less than, or equal to
     */
     public int compareTo(Cat otherCat)
     {
          return getName().compareTo(otherCat.getName());
     }
     
    /**
     * equals determines if another cat is equal to this cat based on ID
     * @param the other cat
     * @return boolean whether they are equal
     */
     public boolean equals(Cat otherCat)
     {
          if (getTag() == otherCat.getTag())
          {
               return true;
          }
          return false;
     }
    
    /**
     * returns string of info about the cat
     * @return info string
     */ 
     public String toString()
     {
          String output = "This cat is named " + getName() + " and it has these values:\n\tEvasion: " + getEvasion() + "\n\tPounce: " + getPounce() + "\n\tTag Number: " + getTag() + "\n";       
          
          return output;
     }
     

     
     /**
      * Default Constructor to build a Cat with Randomly generated Evasion and Pounce Ratings
      */
     public Cat()
     {
          setTag();
          setName("DEFAULT");
          setEvasion(rand.nextInt(11));
          setPounce(rand.nextInt(11));
     }
     
     /**
      * Full Parameter Constructor to build a Cat using the inputed parameter values provided
      * @param inName will be used as the Cat's Name
      * @param inEvade will be used as the Cat's Evasion, if it passes the validity check
      * @param inPounce will be used as the Cat's Pounce, if it passes the validity check
      */
     public Cat(String inName, int inEvade, int inPounce)
     {
          setTag();
          setName(inName);
          setEvasion(inEvade);
          setPounce(inPounce);
     }
     
     /**
      * Copy Constructor to build a Duplicate of the inputted Cat
      * @param inCat is the Cat to be copied by this Cat
      */
     public Cat(Cat inCat)
     {
          setTag();
          setName(inCat.getName());
          setEvasion(inCat.getEvasion());
          setPounce(inCat.getPounce());
     }

     
 
     
     /**
      * setEvasion updates the Cat's evasion rating
      * @param inEvade is the value which will become the Cat's new evasion rating
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
      * setPounce updates the Cat's pounce rating
      * @param inPounce is the value which will become the Cat's new pounce rating
      */
     public void setPounce (int inPounce)
     {
          if (inPounce >= 0 && inPounce <= 10)
          {
               pounce = inPounce;
          }
          else
          {
               System.out.println("Invalid Rating Entered!");
          }

     }

     
     /**
      * getEvasion allows access to the Cat's evasion rating
      * @return the Cat's current evastion rating
      */
     public int getEvasion()
     {
          return evasion;
     }
     
     /**
      * getPounce allows access to the Cat's pounce rating
      * @return the Cat's current pounce rating
      */
     public int getPounce()
     {
          return pounce;
     }
     
     /**
      * pounce will test to see if the cat can successfully catch a particular prey
      * @param inPrey is the prey the cat is trying to pounce on
      * @return the success or failure of the cat's attempt to pounce on the prey
      */ 
     public boolean pounce(Prey inPrey)
     {
          if (inPrey.getEvasion() < getPounce())
          {
               return true; //Got Chomped
          }
          else
          {
               return false; //Didn't get chomped
          }
     }

    public boolean pounce(Prey inPrey, Predator inPartner)
    {
        if (inPrey.getEvasion() < getPounce() + inPartner.getPounce())
        {
           return true; //Got Chomped
        }
        else
        {
           return false; //Didn't get chomped
        }
    }
     
}
