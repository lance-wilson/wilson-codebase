/**
 * The MouseCatDog Class is used to test the implementation of a dequeue of Mouse, Cat and Dog objects.  
 * Checks the push, enqueue, pop, dequeue, peek, contains, size, and toString methods.
 * <br><br>
 * @author Scott Kerlin
 * @author Lance Wilson
 * @version Lab 10
 */
import java.util.Scanner; //Scanner!
import java.util.ArrayList; //ArrayLists!
import java.util.Collections; //Arrays tools
import java.util.Random; //Random!
import java.io.*; //Needed to work with Files!
public class MouseCatDog
{

     public static void main(String[] args)
     {
          AnimalDeque animals = new AnimalDeque();
                   
          //Create File object
          File inFile = new File("Animals.txt"); //Actual name of the file inputted in to File Object Constructor
          
          //Open File for reading using Scanner to Scan the file
          //This could cause a FileNotFoundException, should be handled with a Try/Catch Block
          Scanner inputScanner = null; //If we just declare, Java will complain that it might not be assigned.  So assign to null;
          
          //Try Opening the File
          try
          {
               inputScanner = new Scanner(inFile); //Use the File Object you want to Scan/Read!
          }
          catch (FileNotFoundException e) //If FileNotFoundException is generated
          {
               System.err.println(e.getMessage()); //Print to standard error!
               System.err.println("So, basically your input file is either missing or not named \"Animals.txt\"");
               System.exit(0);
          }
          

          //Scan Cat data while there is still data to read from the Cat input file!
          while(inputScanner.hasNext())
          {
               //Read a line
               String line = inputScanner.nextLine();
               
               //Split (tokenize) the line
               String[] tokens = line.split(","); //Whatever we put into split()'s parameter is what is used to breakup the line
               

               //Use Full Parameter Constructor to create cat1 using tokens
               //Tokens are labelled from 0, starting at the leftmost token
               //Input file should be
               //Box 0, animal type
               //Box 1, name
               //Box 2+ Ratings, evasion 1st if both exist (i.e., a cat!)
               //Integer.parseInt() will take as input a String to convert into a int value
               
               //Determine sub-class
               if (tokens[0].equals("Cat"))  //Is it a cat?
               {
                    // Push cats onto the deque
                    animals.push(new Cat(tokens[1],Integer.parseInt(tokens[2]),Integer.parseInt(tokens[3])));
               }
               //Add more else if statments as needed!
               else if (tokens[0].equals("Mouse"))  //Is it a Mouse?
               {
                    // Enqueue Mice
                    animals.enqueue(new Mouse(tokens[1],Integer.parseInt(tokens[2])));
               }
               else if (tokens[0].equals("Dog"))  //Is it a Dog?
               {
                    // Enqueue Dogs
                    animals.enqueue(new Dog(tokens[1],Integer.parseInt(tokens[2])));
               }
               
          }
          
          
          //Close file by closing the Scanner
          inputScanner.close();

          // Print out Animal Deque
          System.out.println(animals);
          
          //Check peek
          //Should give us Gumball as first, since Gumball was last and was pushed.
          System.out.println("PEEKING! SHOULD BE GUMBALL!");
          System.out.println(animals.peek());
          
          Animal search = animals.peek();
          
          //Check contains works with animal we know is in the list?
          if (animals.contains(search))
          {
               System.out.println("\n\nContains found what we have!");
          }
          else
          {
               System.out.println("\n\nContains DID NOT find what we have!");
          }

          //Remove data
          int size = animals.size();
          Animal removed = animals.pop();
          System.out.println("\n\nRemoved: " + removed);
          size--;
          if (animals.size() == size)
          {
               System.out.println("Size correctly decremented");
          }
          else
          {
               System.out.println("Size NOT correctly decremented");
          }
          
          //Check contains works with animal we know is NOT in the list?
          if (animals.contains(removed))
          {
               System.out.println("\n\nContains found what we SHOULD NOT have!");
          }
          else
          {
               System.out.println("\n\nContains correctly did not find what was removed!");
          }        

          // Remove animals until they're all gone.
          while (animals.size() > 0)
          {
               removed = animals.dequeue();
               System.out.println("\n\nRemoved: " + removed);
               size--;
               if (animals.size() == size)
               {
                    System.out.println("Size correctly decremented");
               }
               else
               {
                    System.out.println("Size NOT correctly decremented");
               }
               
               if (animals.contains(removed))
               {
                    System.out.println("\n\nContains found what we SHOULD NOT have!");
               }
               else
               {
                    System.out.println("\n\nContains correctly did not find what was removed!");
               } 
          }
          
          System.out.println("List should be empty now, printing list again\n");
          System.out.println(animals);





     }
}
