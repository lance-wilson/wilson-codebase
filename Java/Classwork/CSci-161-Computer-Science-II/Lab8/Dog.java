/**
 * The Dog Class is used to simulate a mouse.  
 * A Dog has a name, an evasion rating and a pounce rating.  
 * The evasion rating denotes how good the cat is at escaping dog pounces
 * The pounce rating denotes how good the cat is at pouncing on mice
 * <br><br>
 * @author Lance Wilson
 * @version Lab 8
 */
import java.util.*;
public class Dog extends Animal implements Predator
{

     private int pounce = 0;    //Pounce rating of Dog

     /**
     * compareTo runs the compareTo method on the dog's names
     * @param the other dog
     * @return int whether the name is greater, less than, or equal to
     */
     public int compareTo(Dog otherDog)
     {
          return getName().compareTo(otherDog.getName());
     }
     
    /**
     * equals determines if another dog is equal to this dog based on ID
     * @param the other dog
     * @return boolean whether they are equal
     */
     public boolean equals(Dog otherDog)
     {
          if (getTag() == otherDog.getTag())
          {
               return true;
          }
          return false;
     }
     
    /**
     * returns string of info about the dog
     * @return info string
     */
     public String toString()
     {
          String output = "This dog is named " + getName() + " and it has these values:\n\tPounce: " + getPounce() + "\n\tTag Number: " + getTag() + "\n";

          
          return output;
     }

     /**
      * Default Constructor to build a Dog with Randomly generated Pounce Rating
      */
     public Dog()
     {
          setName("DEFAULT");
          setPounce(rand.nextInt(11));
          setTag();
     }
     
     /**
      * Full Parameter Constructor to build a Dog using the inputed parameter values provided
      * @param inName will be used as the Dog's Name
      * @param inPounce will be used as the Dog's Pounce, if it passes the validity check
      */
     public Dog(String inName, int inPounce)
     {
          setName(inName);
          setPounce(inPounce);
          setTag();
     }
     
     /**
      * Copy Constructor to build a Duplicate of the inputted Dog
      * @param inDog is the Dog to be copied by this Dog
      */
     public Dog(Dog inDog)
     {
          setName(inDog.getName());
          setPounce(inDog.getPounce());
          setTag();
     }
     
     
 
     
     
     /**
      * setPounce updates the Dog's pounce rating
      * @param inPounce is the value which will become the Dog's new pounce rating
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
      * getPounce allows access to the Dog's pounce rating
      * @return the Dog's current pounce rating
      */
     public int getPounce()
     {
          return pounce;
     }
     
     /**
      * pounce will test to see if the Dog can successfully catch a particular prey and pounce on it
      * @param inPrey is the prey the dog is trying to pounce on
      * @return the success or failure of the dog's attempt to pounce on the prey
      */ 
     public boolean pounce(Prey inPrey)
     {
          if (inPrey.getEvasion() < getPounce())
          {
               return true; //Got slobbered
          }
          else
          {
               return false; //Didn't get slobbered
          }
     }

    public boolean pounce(Prey inPrey, Predator inPartner)
    {
        // If the "partner" is a Cat, there's a 50/50 chance the Dog pounces on the Cat
        if (inPartner instanceof Cat && rand.nextBoolean())  //True Randomly selected
        {
            // Dog got distracted and pounces on Cat.
            // Did Cat get pounced on?
            if (pounce((Prey) inPartner))
            {
                //Successfully pounced on partner
                //Original prey gets away
                return false;
            }
            else
            {
                //The Cat evades and is now on its own
                return inPartner.pounce(inPrey);
            }
        }
        else if (inPrey.getEvasion() < getPounce() + inPartner.getPounce())
        {
            //Team Work for the Win!
            return true; //Got Chomped
        }
        else
        {
            return false; //Didn't get chomped
        }
    }
     
}
