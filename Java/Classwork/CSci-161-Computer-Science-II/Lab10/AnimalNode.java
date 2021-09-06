/**
 * @author Lance Wilson
 * @version Lab 10
 */
public class AnimalNode  // Node for storing Animals!
{
    Animal data = null;  // Data!
    AnimalNode next = null;  // Next node in the linked list!

    public AnimalNode(Animal newData)
    {
        setData(newData);
    }


    public void setData(Animal newData)
    {
        data = newData;
    }

    public Animal getData()
    {
        return data;
    }


    public void setNext(AnimalNode newNext)
    {
        next = newNext;
    }

    public AnimalNode getNext()
    {
        return next;
    }


}
