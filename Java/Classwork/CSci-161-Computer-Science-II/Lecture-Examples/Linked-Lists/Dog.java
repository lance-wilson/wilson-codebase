/**
 * The Dog Class is used to simulate a mouse.  
 * A Dog has a name, an evasion rating and a pounce rating.  
 * The evasion rating denotes how good the cat is at escaping dog pounces
 * The pounce rating denotes how good the cat is at pouncing on mice
 * <br><br>
 * @author Scott Kerlin
 * @version Lecture
 */
import java.util.*;
public class Dog extends Animal implements Predator
{

     private int pounce = 0;    //Pounce rating of Dog
     private ArrayList<Dog> puppies = new ArrayList<Dog>();
     
     public void addPuppy(Dog newDog)
     {
          puppies.add(newDog);
     }
     
     public void addPuppies(ArrayList<Dog> litter)
     {
          for (Dog puppy : litter)
          {
               puppies.add(puppy);
          }
     }
     
     public ArrayList<Dog> getPuppies()
     {
          return puppies;
     }
     

     
     public String toString()
     {
          String output = "This dog is named " + getName() + " and it has these values:\n\tPounce: " + getPounce() + "\n\tTag Number: " + getTag() + "\n";
          
          if (puppies.size() == 0)
          {
               output = output + "An No Puppies!!!\n";
          }
          else
          {
               output = output + "And has these puppies:\n-----------------\n";
               for (Dog puppy : puppies)
               {
                    output = output + puppy + "\n\n";
               }
               output = output + "\n-----------------\n";  
          }
          
          
          
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
          for (Dog puppy : inDog.getPuppies())
          {
               puppies.add(new Dog(puppy));
          }
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
     
     public boolean pounce(Prey inPrey, Predator inPartner) throws CannibalismException, DoubleTeamException, StopHittingYourselfException
     {
          if (inPartner.equals(inPrey))
          {
               throw new StopHittingYourselfException();
          }

          if (equals(inPartner))
          {
               throw new DoubleTeamException();
          }
          
          //If a Dog is part of a hunt with a Cat as a predator
          //The Dog may get distracted and pounce on the Cat instead of the original Prey
          //Flip a coin to see if Dog gets distracted
          if (inPartner instanceof Cat && rand.nextBoolean()) //Coin is true; dog was distracted
          {
               
               if (pounce((Prey) inPartner)) //Dog successfully pounces on Cat?
               {
                    return false; //Prey got away
               }
               else //If Cat not pounced on
               {
                    return inPartner.pounce(inPrey); //Cat has to get Prey on own
               }
          }
          else if (inPrey.getEvasion() < (inPartner.getPounce() + getPounce())) //Teamwork!
          {
               return true; //Got 'em!
          }
          else 
          {
               return false; //It got away!
          }
     }
     
 
     public boolean pounce(Prey inPrey)
     {
          if (inPrey.getEvasion() < getPounce())
          {
               return true; //Got 'em!
          }
          else
          {
               return false; //It got away!
          }
     }
     
}
