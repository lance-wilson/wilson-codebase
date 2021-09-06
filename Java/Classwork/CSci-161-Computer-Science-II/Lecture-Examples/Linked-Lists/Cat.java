/**
 * The Cat Class is used to simulate a mouse.  
 * A Cat has a name, an evasion rating and a pounce rating.  
 * The evasion rating denotes how good the cat is at escaping dog pounces
 * The pounce rating denotes how good the cat is at pouncing on mice
 * <br><br>
 * @author Scott Kerlin
 */
import java.util.*;
public class Cat extends Animal implements Prey, Predator
{

     private int evasion = 0;   //Evasion rating of Cat
     private int pounce = 0;    //Pounce rating of Cat

     private ArrayList<Cat> kittens = new ArrayList<Cat>();

     public void addKitten(Cat newCat)
     {
          kittens.add(newCat);
     }

     public void addKittens(ArrayList<Cat> litter)
     {
          for (Cat kitty : litter)
          {
               kittens.add(kitty);
          }
     }

     public ArrayList<Cat> getKittens()
     {
          return kittens;
     }
     

     
     public String toString()
     {
          String output = "This cat is named " + getName() + " and it has these values:\n\tEvasion: " + getEvasion() + "\n\tPounce: " + getPounce() + "\n\tTag Number: " + getTag() + "\n";
          
          if (kittens.size() == 0)
          {
               output = output + "An No Kittens!!!\n";
          }
          else
          {
               output = output + "And has these kittens:\n-----------------\n";
               for (Cat kitten : kittens)
               {
                    output = output + kitten + "\n\n";
               }
               output = output + "\n-----------------\n";  
          }
          
          
          
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
          for (Cat kitten : inCat.getKittens())
          {
               kittens.add(new Cat(kitten));
          }
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
     
      public boolean pounce(Prey inPrey, Predator inPartner) throws CannibalismException, DoubleTeamException, StopHittingYourselfException
     {
          if (equals(inPrey) || inPartner.equals(inPrey))
          {
               throw new StopHittingYourselfException();
          }

          //Check for Cannibalism
          if (inPrey instanceof Cat)
          {
               throw new CannibalismException();
          }
          if (equals(inPartner))
          {
               throw new DoubleTeamException();
          }
          if (inPrey.getEvasion() < (inPartner.getPounce() + getPounce()))
          {
               return true; //Got 'em!
          }
          else 
          {
               return false; //It got away!
          }
     }
     

     public boolean pounce(Prey inPrey) throws CannibalismException, StopHittingYourselfException
     {
          if (equals(inPrey))
          {
               throw new StopHittingYourselfException();
          }
          //Check for Cannibalism
          if (inPrey instanceof Cat)
          {
               throw new CannibalismException();
          }
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
