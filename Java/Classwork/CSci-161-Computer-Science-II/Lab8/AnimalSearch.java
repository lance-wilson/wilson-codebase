/**
 * The AnimalSearch class reads in Animals from a file, and then asks the user if how they would like to search for animals from that list.
 * Searches may be done by ID, name, type, pounce rating range, and evasion rating range.
 * Searching continues until the user enters "no"
 * <br><br>
 * @author Lance Wilson
 * @version Lab 8
 */
import java.util.*;
import java.io.*;

public class AnimalSearch
{
    public static void main(String[] args)
    {
        int selection;  // Search Selection.
        // Variables to search for.
        int upper_pounce, lower_pounce, upper_evasion, lower_evasion, tag;
        String name, type;

        // List of animals
        ArrayList<Animal> animals = new ArrayList<Animal>();

        Scanner keyboard = new Scanner(System.in);
        File animalFile = new File("Animals.txt");
        Scanner fileScanner = null;

        try
        {
            // Try to open scanner
            fileScanner = new Scanner(animalFile);
        }
        catch (FileNotFoundException e)
        {
            System.err.println(e.getMessage());
            System.err.println("Your input file is missing, or not named \"Animals.txt\"");
            System.exit(0); // Nice shutdown
        }  


        // Continue to scan while there is still data in the file
        while(fileScanner.hasNext())
        {
            //Read a line
            String line = fileScanner.nextLine();

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
        fileScanner.close();

        // While loop control
        String again = "yes";

        // Search while user enters yes.
        while (again.equalsIgnoreCase("yes"))
        {
            // Variable to determine if anything was found.
            boolean found_something = false;

            // Ask user how they would like to search.
            System.out.println("How would you like to search?\n\t1: ID/Tag Number\n\t2: Name\n\t3: Type of Animal\n\t4: Pounce Rating range\n\t5: Evasion Rating range");
            selection = keyboard.nextInt();
            keyboard.nextLine();

            // First selection: Search by ID number
            if (selection == 1)
            {
                // Ask for an ID to search for
                System.out.println("Enter an ID number to search for:");
                tag = keyboard.nextInt();
                keyboard.nextLine();

                // Loop through all the animals and print them out if they have that ID number.
                for (Animal animal : animals)
                {
                    if (animal.getTag() == tag)
                    {
                        System.out.println(animal);
                        found_something = true;
                    }
                }
                // If no animals have that tag, found_something is not sent to true, and a message is printed out saying that nothing was found.
                if (!found_something)
                {
                    System.out.println("No animals with that ID number were found.");
                }

                // Ask to search again.
                System.out.println("Would you like to search again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Second selection: Search by name
            if (selection == 2)
            {
                // Ask for name to search for
                System.out.println("Enter a name to search for (case sensitive):");
                name = keyboard.nextLine();

                // Loop through all animals and print them out if they have that name
                for (Animal animal : animals)
                {
                    if (animal.getName().equals(name))
                    {
                        System.out.println(animal);
                        found_something = true;
                    }
                }

                // If no animals have that name, found_something is not sent to true, and a message is printed out saying that nothing was found.
                if (!found_something)
                {
                    System.out.println("No animals with that name were found.");
                }

                // Ask to search again.
                System.out.println("Would you like to search again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Third Selection: Search by Animal type
            if (selection == 3)
            {
                // Ask for type to search for
                System.out.println("Enter a type of animal (Dog, Cat, or Mouse):");
                type = keyboard.nextLine();

                // Loop through all animals
                for (Animal animal : animals)
                {
                    // If the type is a cat
                    if (type.equalsIgnoreCase("cat"))
                    {
                        // If the animal is a Cat, print it
                        if (animal instanceof Cat)
                        {
                            System.out.println(animal);
                            found_something = true;
                        }
                    }

                    // If the type is a Dog
                    if (type.equalsIgnoreCase("dog"))
                    {
                        // If the animal is a Dog, print it
                        if (animal instanceof Dog)
                        {
                            System.out.println(animal);
                            found_something = true;
                        }
                    }

                    // If the type is a Mouse
                    if (type.equalsIgnoreCase("mouse"))
                    {
                        // If the animal is a Dog, print it
                        if (animal instanceof Mouse)
                        {
                            System.out.println(animal);
                            found_something = true;
                        }
                    }
                }

                // If no animals have that type, found_something is not sent to true, and a message is printed out saying that nothing was found.
                if (!found_something)
                {
                    System.out.println("No animals like that were found.");
                }

                // Ask to search again.
                System.out.println("Would you like to search again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Fourth Selection: Search by Pounce Rating Range
            if (selection == 4)
            {
                // Ask for upper bound
                System.out.println("Please enter the upper bound of the Pounce Rating:");
                upper_pounce = keyboard.nextInt();
                keyboard.nextLine();

                // Ask for lower bound
                System.out.println("Please enter the lower bound of the Pounce Rating:");
                lower_pounce = keyboard.nextInt();
                keyboard.nextLine();

                // If lower bound is greater than upper bound, tell the user they messed up and switch the ratings.
                if (upper_pounce <= lower_pounce)
                {
                    System.out.println("\nUpper bound is not greater than lower bound. Ratings will be switched.\n");
                    int temp = upper_pounce;
                    upper_pounce = lower_pounce;
                    lower_pounce = temp;
                }

                // Loop through all the animals
                for (Animal animal : animals)
                {
                    // If the animal is a predator, it will have a pounce rating.
                    if (animal instanceof Predator)
                    {
                        // If the animal is within the range, print it
                        if (((Predator)animal).getPounce() >= lower_pounce && ((Predator)animal).getPounce() <= upper_pounce)
                        {
                            System.out.println(animal);
                            found_something = true;
                        }
                    }
                }

                // If no animals were in that pounce rating range, found_something is not sent to true, and a message is printed out saying that nothing was found.
                if (!found_something)
                {
                    System.out.println("No animals were found in that range of Pounce Ratings were found.");
                }

                // Ask to search again.
                System.out.println("Would you like to search again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Fifth Selection: Search by Evasion Rating Range
            if (selection == 5)
            {
                // Ask for upper bound
                System.out.println("Please enter the upper bound of the Evasion Rating:");
                upper_evasion = keyboard.nextInt();
                keyboard.nextLine();

                // Ask for lower bound
                System.out.println("Please enter the lower bound of the Evasion Rating:");
                lower_evasion = keyboard.nextInt();
                keyboard.nextLine();

                // If lower bound is greater than upper bound, tell the user they messed up and switch the ratings.
                if (upper_evasion <= lower_evasion)
                {
                    System.out.println("\nUpper bound is not greater than lower bound. Ratings will be switched.\n");
                    int temp = upper_evasion;
                    upper_evasion = lower_evasion;
                    lower_evasion = temp;
                }

                // Loop through all animals
                for (Animal animal : animals)
                {
                    // If an animals is a prey, it will have an evasion rating
                    if (animal instanceof Prey)
                    {
                        // If the animal's evasion rating is in the range, print it out
                        if (((Prey)animal).getEvasion() >= lower_evasion && ((Prey)animal).getEvasion() <= upper_evasion)
                        {
                            System.out.println(animal);
                            found_something = true;
                        }
                    }
                }

                // If no animals were in that evasion rating range, found_something is not sent to true, and a message is printed out saying that nothing was found.
                if (!found_something)
                {
                    System.out.println("No animals were found in that range of Evasion Ratings were found.");
                }

                // Ask to search again.
                System.out.println("Would you like to search again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // If selection is not valid.
            if (selection < 1 || selection > 5)
            {
                // Ask if user would like to try again.
                System.out.println("Invalid selection, would you like to try again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

        }

    }
}
