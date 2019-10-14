# Flash SYNTAX v0.3

### Program function
    Program Console; |** This will define that it is console program **|

## Printing
    echo "hello world";
    print "hi";

## Variable declaration
    var number = 14;
### One/Multi Line Comment
    |** This is comment **|

## Input
    var x; |** x = 0 **|
    echo "Enter number:";
    input x;

## Conditional Statments
    if condition {
        |** do something **|
    }
## Repeated Evaluation: Loops
### For Loop:
    var x;
    for x :: x < 10 :: x++ {
        |** do somthing **|
    }
### While Loop
    while condition {
        |** do something **|
    }

## Function Declaration & Calling
### 1. Case
### Function Declaration
> this functiom doesnt take any argument.

    func test : 0 { 
        echo "hello function";
    }

### This is how function is called
    run test;

### 2. Case

### Function Declaration
> This function take argument name. 

    func hello : name {
        echo "Hello" + "\s" + name; |** '\s' will create space **|
    }
### Function Calling

    run hello : Brian;

## Classes, Objects & Methods
#### Flash uses Object Oriented Programming, but not everthing is object.
    Program Console;

    class Person : object {
        func @identity : this, name, age {
            this.name = name
            this.age = age
        } 
        func print : this {
            echo "Hello" + this.name;
        }
    }
    run Person.print : "Brian", 14;