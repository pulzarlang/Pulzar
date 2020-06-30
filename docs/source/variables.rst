Variables
=========

Pulzar, as most of the languages has variables. You can have dynamic, but also staticly typed variables.
Lets take a look at this example::
    var x = 5; \\ You can change the type of variable without any error
    people = True;
    x = "No";
    x = 5i + 3;
    x = 3.14;

As you can see, when you declare variable with keyword var, it will be dynamic - you can change the type without encountering any error.
You can declare also static variables, however you can´t change the type of that variable::
    int a = 5; \\ You can change the type of variable without any error
    people = 3.14; \\ This will give people value 3
    people = "test"; \\ This will cause a TypeError, becuase a was declared as integer not a string

Here is example of all static variable types::

    int points = 50; \\ Integer
    float pi = 3.14159; \\ Float
    complex x = 3i + 5; \\ Complex number
    str name = "John"; \\ String
    char a = 'A'; \\ Character
