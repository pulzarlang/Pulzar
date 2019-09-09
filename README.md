<h1 align = 'center'> Flash programming language (v0.3)</h1>

<div align="center">
  <strong>Flash is modern high-level programming language written in python</strong>
</div>
<br><br>

> Note that Flash is in early stage of development

#### Flash supports both functional & OO programming. It is mostly dynamic language however you can make the code static.
#### In future Flash will also support low level.

## Example of flash v0.3:
```flash
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
<div style="background-image: url('./img/black.jpg');width:600px;height:400px;">
  <code style="color:green;">
    #flash/plugins/flash1.0.1/main.exe<br></code>
    <code style="color:#686868;">
    //My first code</code><br>
    <code class="code1" style="color:lightblue;">Type</code>
  <code class="type_console"> Console</code><code class="normal">;
            <br>
            <br>
             echo </code><code class="inq"> "hello world"</code><code class="normal">;                     
</code>
          </div>
