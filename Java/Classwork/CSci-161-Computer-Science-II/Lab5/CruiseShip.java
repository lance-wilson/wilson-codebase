public interface CruiseShip
{
     int getPass(); //Return current number of Passengers
     int embark(int posPass); //Takes in number of possible passengers, stores as many as will fit on board, returns how many were ABLE to be boarded
     int disembark(); //removes all passengers and returns the number removed from the ship
}