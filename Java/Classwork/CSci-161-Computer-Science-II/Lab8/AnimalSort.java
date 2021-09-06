/**
 * The AnimalSort class reads in Animals from a file, and then asks the user if how they would like to sort the animals from that list.
 * Sorts may be done by: all animals by ID, all animals by name, dogs by pounce rating, mice by evasion rating, and cats by pounce + evasion rating.
 * Searching continues until the user enters "no"
 * <br><br>
 * @author Lance Wilson
 * @version Lab 9
 */
import java.util.*;
import java.io.*;

public class AnimalSort
{
    public static void main(String[] args)
    {
        int selection;  // Search Selection.

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

        // Swap some ID's and add some animals to test code
        Collections.swap(animals, 7, 3);
        Collections.swap(animals, 4, 12);
        Collections.swap(animals, 1, 10);
        animals.add(new Cat("Tom", 7, 3));
        animals.add(new Cat("Jeff", 7, 3));
        animals.add(new Dog("Underdog", 10));
        animals.add(new Mouse("Jasper", 8));
        animals.add(new Dog("Superdog", 10));
        animals.add(new Cat("Arlene", 8, 10));

        // While loop control
        String again = "yes";

        // Search while user enters yes.
        while (again.equalsIgnoreCase("yes"))
        {
            // Variable to determine if anything was found.
            boolean found_something = false;

            // Ask user how they would like to search.
            System.out.println("How would you like to sort?\n\t1: All Animals, by ID/Tag Number (Ascending)\n\t2: All Animals, by Name (Alphabetical)\n\t3: Dogs, by Pounce Rating (descending)\n\t4: Mice, by Evasion Rating (descending)\n\t5: Cats, by Pounce + Evasion Rating (descending)");
            selection = keyboard.nextInt();
            keyboard.nextLine();

            // First selection: Sort by ID number
            if (selection == 1)
            {
                // Sort by ID
                animals = IDSort(animals);

                System.out.println("-----Here are the animals sorted by ascending ID-----\n");
                for (Animal animal : animals)
                {
                    System.out.println(animal);
                }

                // Ask to search again.
                System.out.println("Would you like to sort again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Second selection: Sort by name
            if (selection == 2)
            {
                // Sort by Name
                animals = NameSort(animals);

                System.out.println("-----Here are the animals sorted alphabetically by name (tiebreakers broken by ID)-----\n");
                for (Animal animal : animals)
                {
                    System.out.println(animal);
                }


                // Ask to search again.
                System.out.println("Would you like to sort again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Third Selection: Search by Dogs
            if (selection == 3)
            {
                ArrayList<Dog> dogs = new ArrayList<Dog>();

                int x = 0;
                for (Animal animal : animals)
                {
                    // Create a list of dogs
                    if (animal instanceof Dog)
                    {
                        dogs.add((Dog) animal);
                    }
                }

                Dog unsorted = null;
                int scan;

                // Loop through ArrayList
                for (int index = 1; index < dogs.size(); index++)
                {
                    unsorted = dogs.get(index);
                    scan = index;

                    while (scan > 0 && dogs.get(scan).getPounce() <= dogs.get(scan - 1).getPounce())
                    {
                        if (dogs.get(scan).getPounce() == dogs.get(scan - 1).getPounce())
                        {
                            // Sort by name if pounce are equal
                            if (dogs.get(scan).getName().compareToIgnoreCase(dogs.get(scan - 1).getName()) < 0)
                            {
                                Collections.swap(dogs, (scan - 1), scan);
                            }
                            else if (dogs.get(scan).getName().compareToIgnoreCase(dogs.get(scan - 1).getName()) == 0)
                            {
                                // Sort by ID if names are equal
                                if (dogs.get(scan).getTag() < dogs.get(scan - 1).getTag())
                                {
                                    Collections.swap(dogs, (scan - 1), scan);
                                }
                            }
                        }
                        // Swap dogs if previous dog has higher pounce
                        else if (dogs.get(scan).getPounce() < dogs.get(scan - 1).getPounce())
                        {
                            Collections.swap(dogs, (scan - 1), scan);
                        }
                        scan--;
                    }
                }

                System.out.println("-----Here are the dogs sorted by descending pounce (tiebreakers broken alphabetically by name, then by ID)-----\n");
                for (Dog dog : dogs)
                {
                    System.out.println(dog);
                }

                // Ask to search again.
                System.out.println("Would you like to sort again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Fourth Selection: Search by Mice
            if (selection == 4)
            {
                ArrayList<Mouse> mice = new ArrayList<Mouse>();

                int x = 0;
                for (Animal animal : animals)
                {
                    // Create a list of mice
                    if (animal instanceof Mouse)
                    {
                        mice.add((Mouse) animal);
                    }
                }

                Mouse unsorted = null;
                int scan;

                // Loop through ArrayList
                for (int index = 1; index < mice.size(); index++)
                {
                    unsorted = mice.get(index);
                    scan = index;

                    while (scan > 0 && mice.get(scan).getEvasion() <= mice.get(scan - 1).getEvasion())
                    {
                        if (mice.get(scan).getEvasion() == mice.get(scan - 1).getEvasion())
                        {
                            // Sort by Name if evasion equal
                            if (mice.get(scan).getName().compareToIgnoreCase(mice.get(scan - 1).getName()) < 0)
                            {
                                Collections.swap(mice, (scan - 1), scan);
                            }
                            // Sort by ID if name is equal
                            else if (mice.get(scan).getName().compareToIgnoreCase(mice.get(scan - 1).getName()) == 0)
                            {
                                if (mice.get(scan).getTag() < mice.get(scan - 1).getTag())
                                {
                                    Collections.swap(mice, (scan - 1), scan);
                                }
                            }
                        }
                        // If mouse evasion is less than previous mouse, swap
                        else if (mice.get(scan).getEvasion() < mice.get(scan - 1).getEvasion())
                        {
                            Collections.swap(mice, (scan - 1), scan);
                        }
                        scan--;
                    }
                }

            System.out.println("-----Here are the mice sorted by descending evasion (tiebreakers broken alphabetically by name, then by ID)-----\n");
                for (Mouse mouse : mice)
                {
                    System.out.println(mouse);
                }

                // Ask to search again.
                System.out.println("Would you like to sort again? \"yes\" or \"no\"");
                again = keyboard.nextLine();
            }

            // Fifth Selection: Search by Cat
            if (selection == 5)
            {
                ArrayList<Cat> cats = new ArrayList<Cat>();

                int x = 0;
                for (Animal animal : animals)
                {
                    // Create a list of cats
                    if (animal instanceof Cat)
                    {
                        cats.add((Cat) animal);
                    }
                }

                Cat unsorted = null;
                int scan;

                // Loop through ArrayList
                for (int index = 1; index < cats.size(); index++)
                {
                    unsorted = cats.get(index);
                    scan = index;

                    while (scan > 0 && (cats.get(scan).getPounce() + cats.get(scan).getEvasion()) <= (cats.get(scan - 1).getPounce() + cats.get(scan - 1).getEvasion()))
                    {
                        if ((cats.get(scan).getPounce() + cats.get(scan).getEvasion()) == (cats.get(scan - 1).getPounce() + cats.get(scan -1).getEvasion()))
                        {
                            // Sort by name if the evasion + pounce are equal
                            if (cats.get(scan).getName().compareToIgnoreCase(cats.get(scan - 1).getName()) < 0)
                            {
                                Collections.swap(cats, (scan - 1), scan);
                            }
                            // Sort by ID if the names are equal
                            else if (cats.get(scan).getName().compareToIgnoreCase(cats.get(scan - 1).getName()) == 0)
                            {
                                if (cats.get(scan).getTag() < cats.get(scan - 1).getTag())
                                {
                                    Collections.swap(cats, (scan - 1), scan);
                                }
                            }
                        }
                        // Swap cats if pounce and evasion are less than the previous cats pounce and evasion
                        else if ((cats.get(scan).getPounce() + cats.get(scan).getEvasion()) < (cats.get(scan - 1).getPounce() + cats.get(scan - 1).getEvasion()))
                        {
                            Collections.swap(cats, (scan - 1), scan);
                        }
                        scan--;
                    }
                }

                System.out.println("-----Here are the cats sorted by descending pounce + evasion (tiebreakers broken alphabetically by name, then by ID)-----\n");
                for (Cat cat : cats)
                {
                    System.out.println(cat);
                }
                

                // Ask to search again.
                System.out.println("Would you like to sort again? \"yes\" or \"no\"");
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

    public static <T extends Animal> ArrayList<T> IDSort(ArrayList<T> animals)
    {
        Animal unsorted = null;
        int scan;

        // Loop through ArrayList
        for (int index = 1; index < animals.size(); index++)
        {
            unsorted = animals.get(index);
            scan = index;

            // While the unsorted animal's ID is greater than the previous animal, swap them
            while (scan > 0 && animals.get(scan).getTag() < animals.get(scan - 1).getTag())
            {
                Collections.swap(animals, (scan - 1), scan);
                scan--;
            }
        }

        return animals;
    }

    public static <T extends Animal> ArrayList<T> NameSort(ArrayList<T> animals)
    {
        Animal unsorted = null;
        int scan;

        for (int index = 1; index < animals.size(); index++)
        {
            unsorted = animals.get(index);
            scan = index;

            while (scan > 0 && animals.get(scan).getName().compareToIgnoreCase(animals.get(scan - 1).getName()) < 0)
            {
                // If the names are equal, sort by ID
                if (animals.get(scan).getName().compareToIgnoreCase(animals.get(scan - 1).getName()) == 0)
                {
                    IDSort(animals);
                }
                // If the name is greater than the previous animal, swap them
                else if (animals.get(scan).getName().compareToIgnoreCase(animals.get(scan - 1).getName()) < 0)
                {
                    Collections.swap(animals, (scan - 1), scan);
                    scan--;
                }
            }
        }

        return animals;
    }
}
