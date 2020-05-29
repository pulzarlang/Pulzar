 <div align="center"><h1>Pulzar Programming language v0.4</h1></div>

<div align="center">
  <strong>Pulzar is new experimental programming language that has flexible syntax and gives freedom to the programmer. In future it would try to foucus on quantum computing.</strong>
</div>
<br><br>

> Note that Pulzar is in early stage of development

#### Pulzar supports both functional & OO programming. It supports both static and dynamic typing. The staticlly typed variables have strong typing.
#### The latest version can be both runnned at run time or be compiled to executable

## Example of Pulzar v0.4:
```pulzar
  Program Console;
  include math;
 |** This is comment **|
  int n = 5!;
  var boolean = False;
  var x = 10;
  echo n;
  if x mod 2 == 0 {
      echo "Yes";
      if x != 10 {
          echo "Not good";
      }
  }
 
  var i, a;
  for i :: i < 10 :: ++i {
      a = i ** 2 / (2**i - i);
      echo x;
  }
  func circle : r { 
      echo pi * r ** 2;
  }

  func print_name : name 
  {
      echo "Hello" + "\s" + name;
  }
  print "Enter r:";
  input a;
  circle : a;
  echo "Enter name:";
  input b;
  print_name : b;
```
### Pulzar v0.4 priority is to colaborate LLVM with it for speed.



## Features

This are feautures what pulzar can do now:
- [x] printing
- [x] input
- [x] Variable declaration 
- [x] Variable definition
- [x] Arrays
- [x] Math 
- [x] If statements
- [x] Else statements
- [x] Else if statements
- [x] Nested Conditional statements
- [x] For loops
- [x] While loop
- [x] Nested loops
- [x] Functions 
- [x] Function calls 
- [x] Math library
- [x] Imports libaries & files
- [ ] Pointers
- [ ] Macros
- [ ] OOP

## Contribiution
All contribution will be highly appreciated and might be rewarded.