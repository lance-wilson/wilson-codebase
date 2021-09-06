public class Driver
{
     public static void main(String[] args)
     {
          //Need an array of boats
          Watercraft[] boats = new Watercraft[6];
          
          //Build 2 barges
          boats[0] = new Barge("La Rosa", 100000);  //Name, max pounds of cargo
          boats[1] = new Barge("Waterlily", 200000);
                    
          //Build 2 yachts
          boats[2] = new Yacht("Gadfly", 120);  //Name, max passengers
          boats[3] = new Yacht("Step-Sister", 20);
          
          //Build 2 caravels
          boats[4] = new Caravel("Santa Maria", 50, 300000);  //Name, max passengers, max pounds of cargo
          boats[5] = new Caravel("Nina", 20, 150000);
          
          //Build 2 ports
          Port[] berths = {new Port("High Water"), new Port("Low Water")};
          
          //Assume all boats start at Low Water, go to High Water, and then will comeback to Low Water to start their next trip.
          //Move all people and goods from Low Water to High Water
          int allGoods = berths[0].getCargo() + berths[1].getCargo();
          int allPeople = berths[0].getPass() + berths[1].getPass();
          //Count the Trips
          int trips = 0;
          while(berths[0].getCargo() != allGoods || berths[0].getPass() != allPeople)
          {
               System.out.println("\n-----TRIP " + trips + " -----");
               System.out.println("\t" + berths[1].getCargo() + " pounds of goods need to be moved.");
               System.out.println("\t" + berths[1].getPass() + " people need to be moved.");
               //Load Ships at Low Water
               for (Watercraft ship : boats)
               {
                    String message = ship.getName() + " has been loaded with:\n";
                    //Load Passengers, if able
                    if (ship instanceof CruiseShip)
                    {
                        berths[1].loadPass((CruiseShip) ship);
                        message = message + "\tPassengers: " + ((CruiseShip) ship).getPass();
                    }
                    
                    //Load Cargo, if able...Note the separate if since some Watercraft can do both
                    if (ship instanceof CargoShip)
                    {
                         berths[1].loadCargo((CargoShip) ship);
                         message = message + "\tCargo: " + ((CargoShip) ship).getCargo();
                    }
                    System.out.println(message);
               }
                                  
               //Unload the Ships at High Water
               for (Watercraft ship : boats)
               {
                    //Unload Passengers, if able
                    if (ship instanceof CruiseShip)
                    {
                        berths[0].unloadPass((CruiseShip) ship);
                    }
                    
                    //unload Cargo, if able...Note the separate if since some Watercraft can do both
                    if (ship instanceof CargoShip)
                    {
                         berths[0].unloadCargo((CargoShip) ship);
                    }
               }
               
               trips++;
          }
          System.out.println ("\n\n-----COMPLETED ON TRIP " + trips + "-----");
     }
}