/**
 * The Animal Class is used to simulate an animal.  
 * A Animal has a name and an ID.  
 * <br><br>
 * @author Lance Wilson
 * @version Lab 8
 */
import java.util.*;
public class Animal
{
     private static int regID = 0; //Next ID
     private int tag = 0;       //ID for this Animal
     private String name = "";  //Name of Animal
     protected Random rand = new Random();

    /**
     * setTag sets the ID number of the animal
     */
     protected void setTag()
     {
          tag = regID;
          regID++;
     }
     
    /**
     * getTag allows access to the ID number
     * @return the integer ID
     */
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

}
