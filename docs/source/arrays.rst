Array
=====
An array is data structure that can store multiple values of in a single variable.

Array in pulzar look like this::

    var array;
    array = [1, 3, 5, 7, 9];

The size of the array can be defined although it is optional::

    char alphabet[26] = ['A', 'B', 'C', 'D' 'E', ... , 'Z'];

Printing all elements of an array is simple as that::

    int array = [1, 3, 5, 7, 9];
    echo array;

You can also loop through each element with in keyword::

    int array = [1, 3, 5, 7, 9];
    int i;
    for i in array {
        echo i;
    }

You can also do this by more traditional way::

    str cars = ["BNW", "Lamborgini", "Ford", "Porsche"];
    int i;
    for i :: i < 4 :: i++ {
        echo cars[i];
    }

Multi dimentional array::

    var matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    for cell in matrix {
        for i in cell {
            echo i;
        }
    }
