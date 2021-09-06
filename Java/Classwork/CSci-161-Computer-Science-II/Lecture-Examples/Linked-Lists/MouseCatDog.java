/**
 * The MouseCatDog Class is used to test out the Mouse, Cat and Dog objects.  
 * Eventually, this will become the driver for a program which will simulate the interactions of Mice, Cats and Dogs.
 * <br><br>
 * @author Scott Kerlin
 * @author Lance Wilson
 * @version Lecture 23
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
          //I have no idea how many Animals will be in the file, so just gonna start with an empty ArrayList.
          //ArrayList <Animal> animals = new ArrayList<Animal>();
          //SingleLinkedList animals = new SingleLinkedList();
          //DoubleLinkedList animals = new DoubleLinkedList();
          //CircularLinkedList animals = new CircularLinkedList();
          CircularDoubleLinkedList animals = new CircularDoubleLinkedList();
          
          
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
                    animals.add(new Cat(tokens[1],Integer.parseInt(tokens[2]),Integer.parseInt(tokens[3])));
               }
               //Add more else if statments as needed!
               else if (tokens[0].equals("Mouse"))  //Is it a Mouse?
               {
                    animals.add(new Mouse(tokens[1],Integer.parseInt(tokens[2])));
               }
               else if (tokens[0].equals("Dog"))  //Is it a Dog?
               {
                    animals.add(new Dog(tokens[1],Integer.parseInt(tokens[2])));
               }
               
          }
          
          
          //Close file by closing the Scanner
          inputScanner.close();
  
          //Let's just print the data out of the ArrayList to see what we've read. 
          //Since I don't do anything with non-cats yet, I should only get Cat data at this point
          
          System.out.println(animals);
          
          //Check get with front and back of list, and that we get nulls for bad indices
          //Should give us Jerry as first and Gumball as last
          System.out.println("PRINTING FIRST! SHOULD BE JERRY!");
          System.out.println(animals.get(0));
          
          System.out.println("\n\nPRINTING LAST! SHOULD BE GUMBALL!");
          System.out.println(animals.get(animals.size() - 1));
                             
          if (animals.get(-1) == null && animals.get(animals.size()) == null)
          {
               System.out.println("\n\nBoth bad indices gave null");
          }
          else
          {
               System.out.println("\n\nOne or more bad indices DID NOT give null");
          }

          
          //Check contains works with animal we know is in the list?
          if (animals.contains(animals.get(3)))
          {
               System.out.println("\n\nContains found what we have!");
          }
          else
          {
               System.out.println("\n\nContains DID NOT find what we have!");
          }

          //Remove data
          int size = animals.size();
          Animal removed = animals.remove(4);
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

          //Bad remove testing!
          if (animals.remove(-1) == null && animals.remove(animals.size()) == null)
          {
               System.out.println("\n\nBoth bad REMOVE indices gave null");
          }
          else
          {
               System.out.println("\n\nOne or more bad REMOVE indices DID NOT give null");
          }

          //Randomly remove until empty!
          Random rand = new Random();
          while (animals.size() > 0)
          {
               removed = animals.remove(rand.nextInt(animals.size()));
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
