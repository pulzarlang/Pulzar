Array
=====

In pulzar you can create an array like this::

    var array;
    array = [1, 3, 5, 7, 9];

The size of the array can be defined although it is optional::

    char alphabet[26] = ['A', 'B', 'C', 'D' 'E', ... , 'Z'];

Printing all elements of an array is simple as that::

    int array = [1, 3, 5, 7, 9];
    echo array;

You can also loop through each element like this::

    int array = [1, 3, 5, 7, 9];
    int i;
    for i :: i < 5 :: i++ {
        echo array[i];
    }
