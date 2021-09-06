public class DoubleLinkedList
{
     private int size = 0;  //Number of items in the list
     private AnimalNode head = null; //Head of list
     private AnimalNode tail = null; //Back of list

     public void add(Animal data)  //Add to back of list
     {
        if (tail == null) //Empty List
        {
            tail = new AnimalNode(data);  
            head = tail;
        }
        else
        {
            //All other cases, just add to tail
            tail.setNext(new AnimalNode(data));
            AnimalNode prev = tail.getNext();
            tail = tail.getNext();
            tail.setPrev(prev);
        }
        size++;
     }

     public Animal remove(int index)  //Remove at index
     {
        if (index < 0 || index >= size) //Invalid indices?
        {
            return null;
        }

        if (index == 0) // Working with head
        {
            AnimalNode target = head;
            head = head.getNext();
            if (head != null)
            {
                head.setPrev(null);
            }
            target.setNext(null);
            target.setPrev(null);
            size--;
            if (target == tail) //Tail check!
            {
                tail = null; 
            }
            return target.getData();
        }

        // Not head
        AnimalNode curr = head;
        int counter = 1;
        while (counter != index)  //Move curr to one node BEFORE target
        {
            curr = curr.getNext();
            counter++;
        } 
        AnimalNode target = curr.getNext();
        curr.setPrev(curr);
        curr.setNext(target.getNext()); 
        target.setNext(null);
        target.setPrev(null);
        size--;
        if (target == tail)  //Deal with tail
        {
            tail = curr;
        }
        return target.getData();

     }
     
     public boolean contains(Animal target) //Check if a specific Animal is in the list
     {
        AnimalNode curr = head; //Start at head
        while(curr != null) //As long as there are more nodes
        {
            if (curr.getData().equals(target))
            {
                return true;
            }
            curr = curr.getNext();
        }
        return false;//Got through entire list, didn't find the animal
     }
     
     public String toString()
     {
        String output = "There are: " + size() + " elements in this list\n\n";
        AnimalNode curr = head; //Start at head
        while(curr != null) //As long as there are more nodes
        {
            output = output + curr.getData() + "----------\n";
            curr = curr.getNext();
        }
        return output;
     }
     
     public Animal get(int index) //Get animal from a location
     {
        if (index < 0 || index >= size) //Bad indices
        {
           return null;
        }

        AnimalNode curr = tail; //Start at head
        for (int x = size; x > index; x--) //Go to index
        {
            curr = curr.getPrev();
        }

        return curr.getData();
          
     }

     public int size() //return size
     {
        return size;
     }
}











