public interface Predator
{
     
     //Standardize gets and sets
     void setPounce(int inPounce);
     int getPounce();

     //Standardize pouncing!
     //One-on-one Predator versus Prey
     boolean pounce(Prey inPrey) throws CannibalismException, StopHittingYourselfException;
     //Hunting with a partner
     boolean pounce(Prey inPrey, Predator inPartner) throws CannibalismException, DoubleTeamException, StopHittingYourselfException; 

}