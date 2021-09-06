/**
 * @author Lance Wilson
 * @version Lab 9
 */

import java.util.*;
public class Animal implements Comparable<Animal>
{
     private static int regID = 0; //Next ID
     private int tag = 0;       //ID for this Animal
     private String name = "";  //Name of Animal
     protected Random rand = new Random();

     protected void setTag()
     {
          tag = regID;
          regID++;
     }
     
     public int getTag()
     {
          return tag;
     }

    /**
      * setName updates the Animals's name
      * @param inName is the String that will become the Animal's new name
      */
     public void setName(String inName)
     {
          name = inName;
     }

     
     /**
      * getName allows access to the Animal's name
      * @return the Animal's current name
      */
     public String getName()
     {
          if (name.equals(""))
          {
               return "No Name Set";
          }
          else
          {
               return name;
          }
     }
     
     public int compareTo(Animal otherAnimal)
     {
          return getName().compareTo(otherAnimal.getName());
     }
     
     public boolean equals(Animal otherAnimal)
     {
          if (getTag() == otherAnimal.getTag())
          {
               return true;
          }
          return false;
     }

}
