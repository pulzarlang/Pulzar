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

Operations with dynamic variables::

    var x = 5;
    echo x / 2; \\ output: 2.5
    echo x / 7; \\ output: 0.7142857142857143
    echo x ^ 2; \\ output: 25

When the variables are declared dynamically, you can change their type, e. g. type : (x) = int, type : (x / 2) = float.

Operations with static variables::

    int a = 31;
    echo xa / 3; \\ output: 10, not 10.333333...


When you declare statically variable, however the values's type wont be changed, e. g. type : (a) = int, type : (a / 3) = int.
