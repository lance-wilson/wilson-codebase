public class AnimalNode
{
    private Animal data = null; //Data
    private AnimalNode next = null; //Memory Reference to next Node in List
    private AnimalNode prev = null;

    public AnimalNode(Animal newData) //Constructor, package data into a node
    {
        setData(newData);
    }

    public void setNext(AnimalNode nextNode)
    {
        next = nextNode;
    }

    public AnimalNode getNext()
    {
        return next;
    }

    public void setPrev(AnimalNode prevNode)
    {
        prev = prevNode;
    }

    public AnimalNode getPrev()
    {
        return prev;
    }

    public void setData(Animal newData)
    {
        data = newData;
    }

    public Animal getData()
    {
        return data;
    }

 
}
