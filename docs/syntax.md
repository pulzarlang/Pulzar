# Pulzar SYNTAX v0.4

<link rel="stylesheet" type="text/css" href="code.css">

## Program definition
### Console
<div style="background-color:#181818">
    <code class="code1">
        <span class="func">Program </span><span class="normal">Console; </span><br>
    </code>
</div>

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
</code>
</div>

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
<div style="background-color : #181818">
<code class="code1">
 <span class="comment">\\ This is a single line comment in Pulzar</span><br>
</code>
</div>

### One/ Multy line comment
<div style="background-color : #181818">
<code class="code1">
 <span class="comment">|* <br> This is a multy line comment in Pulzar <br> *|</span><br>
</code>
</div>

## Input
    int x; |** define x = 0 **|
    echo "Enter number:";
    input x;



## Conditional Statments
<div style="background-color : #181818">
<code class="code1">
    <span class="func">if</span><span class="normal"> condition<span> {</span><br>
        <span style="margin-right:1.66rem"></span>        <span class="comment">|** do somthing ... **|    </span><br>
        <span class="normal">}</span>
        </code>
</div>

## Repeated Evaluation: Loops
### For Loop:
<div style="background-color : #181818">
    <code class="code1">
        <span class="func">int</span><span class="normal"> x;</span><br>
        <span class="func">for</span><span class="normal"> x</span><span class="symbol"> :: </span><span class="normal">x</span><span class="symbol"> <= </span><span class="num">10</span><span class="symbol"> ::</span><span class="normal"> x++ {</span><br>
        <span style="margin-right:1.66rem"></span>        <span class="func">echo</span><span class="normal"> x</span><span class="symbol"> **</span><span class="num"> 2</span><span class="normal">;</span><br>
        <span class="normal">}</span>
        </code>
</div>

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
    100

### While Loop
<div style="background-color : #181818">
    <code class="code1">
        <span class="func">while</span><span class="normal"> condition<span> {</span><br>
        <span style="margin-right:1.66rem"></span>                          <span class="comment">|** do somthing ... **|</span><br>
        <span class="normal">}</span>
        </code>
</div>

## Function Declaration & Calling
### 1. Case
### Function Declaration
> this function doesnt take any argument.

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
    run Person.print : "Brian", 14;

#### Output:
    Hello Brian
    You are 14
