public interface CargoShip
{
     int getCargo(); //Return current pounds of Cargo
     int load(int posCargo); //Takes in possible pounds of cargo to load, stores the cargo, returns how many pounds of cargo were ABLE to be loaded
     int unload(); //Removes all the cargo, returns the pounds of cargo removed
}