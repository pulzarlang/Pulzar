Getting started
===============
In order to start using pulzar, you need download and install it on your device. You can donwnload pulzar on https://pulzar.org/web/download/ or just clone github repository.
When you open pulzar, a ineractive console will pop up, where you can easily experiment with pulzar::

   (c) Brian Turza 2018 - 20 Pulzar v0.4

   Welcome to

        ____        __
      / __ \__  __/ /___  ____ ______
     / /_/ / / / / /_  / / __ `/ ___/
    / ____/ /_/ / / / /_/ /_/ / /
   /_/    \__,_/_/ /___/\__,_/_/


   Type 'help' for more information
   >echo "test";
   test
   >

You can exit interactive shell by typing exit().
When you create .plz script and you want to run without shell, put name of file you want to run::
    ~$ pulzar test.plz

Hello world
===========
Making hello world in pulzar is really simple::

    Program Console;
    echo "hello world";

This will result hell world.

if you want to see all tools and how pulzar works add -t argument after filename::

    ~$ pulzar test.plz -t