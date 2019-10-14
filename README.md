<h1 align = 'center'> Pulzar programming language (v0.4)</h1>

<div align="center">
  <strong>Pulzar is modern  programming language with both high and low level features.</strong>
</div>
<br><br>

> Note that  is in early stage of development

#### Pulzar supports both functional & OO programming. It is mostly dynamic language however you can make the code static.
#### In future Pulzar will also support low level.

## Example of Pulzar v0.4:
```pulzar
  Program Console;
  include math;
 |** This is comment **|
  int n = 5!;
  var bool = False;
  var x = 10;
  echo n;
  if x != 10 {
    echo "Not good";
  }
  var i;
  for i :: i < 10 :: ++i {
    x = i ** 2 / (2**i - i);
    echo x;
  }
  func circle : r { 
      echo pi * r ** 2;
  }

  func print_name : name 
  {
      echo "Hello" + "\s" + name;
  }
  echo "Enter r:";
  int a -> input;
  run circle : a;
  echo "Enter name:";
  str b -> input;
  run print_name : b;
```
### Pulzar v.04 is working mostly on better AST and use of LLVM.


## Features

This are feautures what pulzar can do now:
- [x] printing
- [x] input
- [x] Variable declaration 
- [x] Variable definition
- [x] Math 
- [x] If statments
- [x] Else statments
- [x] Else if statments
- [x] For loops
- [x] While loop
- [x] Functions 
- [x] Function calls 
- [ ] Math library ( working on it)
- [ ] Imports libaries
- [ ] Pointers
- [ ] Macros

