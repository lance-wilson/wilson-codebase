/**
 * The AnimalDeque class is used to store methods relating to the use of a Deque (Queue + stack) of Animals. It has methods used both by queues and by stacks. It has a head, a tail, and a size.
 * @author Lance Wilson
 * @version Lab 10
 */
public class AnimalDeque   // Deque of Animals
{

    int size = 0; // How much is in the list?
    AnimalNode tail = null;  // Start with no tail
    AnimalNode head = null;  // Start with no head

    /**
     * The size method allows access to the size of the Deque
     * @return the size.
     */
    public int size() // Return current size
    {
        return size;
    }

    /**
     * enqueue adds an Animal to the back of the list.
     * @param The Animal to be added.
     */
    public void enqueue(Animal data)  // Add to the end
    {
        // Empty list
        if (tail == null)
        {
            tail = new AnimalNode(data);
            head = tail;
        }
        else // Add to tail
        {
            tail.setNext(new AnimalNode(data));
            tail = tail.getNext();
        }

        size++;
    }

    /**
     * dequeue removes the Animal at the front of the list and returns it.
     * @return The Animal removed
     */
    public Animal dequeue()
    {
        // Remove front of list Head
        AnimalNode target = head;
        head = head.getNext();
        target.setNext(null);
        size--;
        return target.getData();
    }

    /**
     * Push adds an Animal to the Top of the list
     * @param The Animal to add to the Deque
     */
    public void push(Animal data)
    {
        if (tail == null)
        {
            tail = new AnimalNode(data);
            head = tail;
        }
        else
        {
            AnimalNode newHead = new AnimalNode(data);
            newHead.setNext(head);
            head = newHead;
        }

        size++;
    }

    /**
     * Pop removes an Animal from the Top of the list.
     * @return The Animal removed
     */
    public Animal pop()
    {
        AnimalNode target = head;
        head = head.getNext();
        target.setNext(null);
        size--;
        return target.getData();
    }

    /**
     * Peek looks at the Animal that will be next to be removed, and returns it without removing it.
     * @return The next animal to be removed (the head).
     */
    public Animal peek()
    {
        return head.getData();
    }

    /**
     * Contains takes in an animal and searches the deque for that animal, and returns a boolean stating whether it was found.
     * @param search is the Animal to search for
     * @return found is the boolean value of whether it was found.
     */
    public boolean contains(Animal search)
    {
        AnimalNode curr = head;
        boolean found = false;

        for (int y = 0; y < size(); y++)
        {
            if (curr.getData().equals(search))
            {
                found = true;
            }
        }

        return found;
    }

    /**
     * toString returns a string containing all of the individual animals toStrings, plus the size of the deque.
     * @return the information string.
     */
    public String toString()
    {
        AnimalNode curr = head;

        String output = "";
        if (curr != null)
        {
            for (int x = 0; x < size(); x++)
            {
                output = output + curr.getData().toString() + "\n";
                curr = curr.getNext();
            }
        }
        else
        {
            output = "NO ANIMALS!\n";
        }

        return "This deque has a size of " + size() + " and contains the following animals:\n\n" + output;
    }

}
