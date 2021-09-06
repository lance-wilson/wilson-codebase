/**
 * Predator interface determines whether an animal can be considered a predator
 * @author Lance Wilson
 * @version Lab 9
 */
public interface Predator
{
    int getPounce();
    void setPounce(int inPounce);
    boolean pounce(Prey inPrey);
    boolean pounce(Prey inPrey, Predator inPartner);
}
