# Pulzar SYNTAX v0.4


## Program definition
### Console
    Program Console;

## Printing 
### Echo function
> Echo function after printing makes a new line

    echo "hello world";
    echo "hello universe";

#### Output:
    hello world
    hello universe

### Print function
> Print function after printing doesnt make a new line

    print "Hello" + "\s";
    print "Dave";

#### Output:
    Hello Dave

## Variable declaration
#### Pulzar has both dynamic and static datatyping
### Dynamic typing
    var x = 10;

### Static typing
    
    str name = "Brian Turza";
    int age = 14;
    bool isPulzar = True;
    float pi = 3.14159;

## Comments
### Single line
    \\ This is a single line comment in Pulzar


### One/ Multy line comment

    |* This is a 
    multi line comment
     in Pulzar *|

## Input
    int x; |** define x = 0 **|
    echo "Enter number:";
    input x;



## Conditional Statments
    if condition {
        |** Do somthing... **|
    }

## Repeated Evaluation: Loops
### For Loop:
    int x;
    for x :: x < 10 :: x++ {
        echo x ** 2;
    }

#### Output:
    0
    1
    4
    9
    16
    25
    36
    49
    64
    81
### While Loop
    while condtion {
        |** Do somthing **|
    }

## Function Declaration & Calling
### 1. Case
### Function Declaration
> this function doesnt take any argument.

    func test : () {
        int array = [1 , 3, 5, 7, 9];
        int i;
        for i :: i < 4 :: i++ {
            echo (array[i] + 1) ** 2;
        }
    }

### This is how function is called
    test : ();

#### Output:
    4
    16
    36
    64
    100
 
### 2. Case

### Function Declaration
> This function take argument name. 

    func hello : name {
        echo "Hello" + "\s" + name; |** '\s' will create space **|
    }
### Function Calling

    hello : Brian;

## Classes, Objects & Methods
#### Pulzar has Object Oriented Programming feautures
    Program Console;

    class Person : object {
        func @identity : this, name, age {
            str this.name = name;
            int this.age = age;
        } 
        func print : this {
            echo "Hello" + this.name;
            echo "You are" + "\s" + this.age;
        }
    }
    Person.print : "Brian", 14;

#### Output:
    Hello Brian
    You are 14
