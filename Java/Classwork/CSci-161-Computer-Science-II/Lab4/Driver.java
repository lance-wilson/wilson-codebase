/**
 * The Driver class is used to demonstrate the methods in the Car and FuelGauge objects.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 4
 */

import java.util.Random;

public class Driver
{
    public static void main(String[] args)
    {
        // Random number generator to decide number of trips later.
        Random rand = new Random();

        // Create an array of cars, then create two new cars to put in the array.
        Car[] car = new Car[3];
        car[0] = new Car();
        car[1] = new Car();

        // Print out the stats of the cars and their fuel gauges.
        System.out.println(car[0]);
        System.out.println(car[0].getFuelGauge());
        System.out.println(car[1]);
        System.out.println(car[1].getFuelGauge());

        // Use the compareTo method in FuelGauge to compare the percentage of fuel left in each car, and print the result of this comparison.
        System.out.println("Now comparing the fuel gauges.");
        if (car[0].getFuelGauge().compareTo(car[1].getFuelGauge()) == 0)
        {
            System.out.println("The car's fuel gauges have the same percentage of fuel left.\n\n");
        }
        else if (car[0].getFuelGauge().compareTo(car[1].getFuelGauge()) == 1)
        {
            System.out.println("Car 0 has a greater percentage of fuel remaining.\n\n"); 
        }
        else if (car[0].getFuelGauge().compareTo(car[1].getFuelGauge()) == -1)
        {
            System.out.println("Car 1 has a greater percentage of fuel remaining.\n\n");
        }

        // Send each car on a random number of trips to demonstrate the drive() method.
        for (int i = 0; i < 2; i++)
        {
            int trips = rand.nextInt(10);
            System.out.println("Car " + i + " will take attempt to take " + trips + " trips.");
            for (int j = 0; j < trips; j++)
            {
                car[i].drive();
            }
            System.out.println("\n");
        }

        // Copy car 0.
        System.out.println("A copy of car 0 will be created.\n");
        car[2] = new Car(car[0]);
        
        // Print stats again.
        System.out.println(car[0]);
        System.out.println(car[0].getFuelGauge());
        System.out.println(car[1]);
        System.out.println(car[1].getFuelGauge());
        System.out.println(car[2]);
        System.out.println(car[2].getFuelGauge());

        // Send each car on a few more trips
        for (int i = 0; i < 3; i++)
        {
            int trips = rand.nextInt(10);
            System.out.println("Car " + i + " will take attempt to take " + trips + " more trips.");
            for (int j = 0; j < trips; j++)
            {
                car[i].drive();
            }
            System.out.println("\n");
        }

        // Print stats again.
        System.out.println(car[0]);
        System.out.println(car[0].getFuelGauge());
        System.out.println(car[1]);
        System.out.println(car[1].getFuelGauge());
        System.out.println(car[2]);
        System.out.println(car[2].getFuelGauge());

        // Check to make sure cars are equal. None of them should be, since the registration numbers for each should be different.
        System.out.println("The cars will now be checked for equality.");
        if (car[0].equals(car[1]))
        {
            System.out.println("Car 0 is equal to Car 1.");
        }
        else
        {
            System.out.println("Car 0 is not equal to car 1.");
        }

        if (car[1].equals(car[2]))
        {
            System.out.println("Car 1 is equal to Car 2.");
        }
        else
        {
            System.out.println("Car 1 is not equal to car 2.");
        }

    }
}
