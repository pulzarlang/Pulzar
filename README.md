<h1 align = 'center'> Pulzar programming language (v0.3)</h1>

<div align="center">
  <strong>Pulzar is modern high-level programming language written in python</strong>
</div>
<br><br>

> Note that  is in early stage of development

#### Pulzar supports both functional & OO programming. It is mostly dynamic language however you can make the code static.
#### In future Pulzar will also support low level.

## Example of Pulzar v0.3:
```pulzar
  Program Console;
  include math;
 |** This is comment **|
  factorial 5;
  var bool = False;
  var x = 10;
  if x != 10 {
    echo "Not good";
  }
  var i;
  for i :: i < 10 {
    x /= x -1
  }
  func circle : r { 
      echo pi * r ** 2;
  }

  func print_name : name 
  {
      echo "Hello" + "\s" + name;
  }
  echo "Enter r:";
  input a :: int;
  run circle : a;
  echo "Enter name:";
  input b :: str;
  run print_name : b;
```
