import java.util.Random;
public class Port
{
     private String name;
     private int goods;
     private int people;
     private Random rand = new Random();
     
     public Port(String inName)
     {
          setName(inName);
          setCargo(rand.nextInt(8000000) + 1000000);
          setPass(rand.nextInt(50000) + 10000);
          
     }
     
     public String getName()
     {
          return "Port " + name;
     }
     
     private void setPass (int inPass)
     {
          if (inPass >= 0 )
          {
               people = inPass;
          }
     }
     
     public void unloadPass(CruiseShip shipP)
     {
          setPass(getPass() + shipP.disembark());
     }
     
     public void loadPass (CruiseShip shipP)
     {
          setPass(getPass() - shipP.embark(getPass()));
     }     
     
     private void setCargo (int inCargo)
     {
          if (inCargo >= 0 )
          {
               goods = inCargo;
          }
     }
     
     public void unloadCargo(CargoShip shipC)
     {
          setCargo(getCargo() + shipC.unload());
     }
     
     public void loadCargo (CargoShip shipC)
     {
          setCargo(getCargo() - shipC.load(getCargo()));
     }
     
     public void setName(String inName)
     {
          name = inName;
     }
     
     public int getCargo()
     {
          return goods;
     }
     
     public int getPass()
     {
          return people;
     }
     
     public String toString()
     {
          return getName() + " has:\n\tGoods: " + getCargo() + "\n\tPeople: " + getPass();
     }
}