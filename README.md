# Tabular-C++
#### by Matthew Smith
## Overview
Tabular-C++ is a library and toolset to implement tables in C++. It is intended to help with building software using table-based relational models. 

In software design, it is easy to be held back by the paradigm one is using. 
For all its merits, many are throwing harsh criticism at the object-oriented style for its shortcomings.
The argument is that object-oriented programming is both unstable to refactoring, and due to its hierarchical structure can be both cumbersome to work with, not even mentioning performance penalties. 

An alternative to object-oriented programming, is to organise data into tables. 
Here, data exists in a purer form, not locked away by objects. 
This facilitates a more data-oriented style, with a clear separation between data and logic.
Any relationship between data can be expressed by occupation of the same row of some table. Unfortunately, due to its static typing, tables are not easy to implement in C++ (as far as I can tell at least).

That is where Tabular-C++ comes in, With the use of generic table-building macros, as well as a basic Python script, Tabular-C++ can build class implementations of tables from information provided by a user-created Python module.

## Guide
For a full guide on how to start using Tabular-C++, check out the [Tabular-C++ Guide](guide/introduction.html).  

There, you can learn in-depth how to construct tables in this framework (there's more than one way), and all the different ways you can use them. 

## Basic Example

#### include/example/example.hpp

    #pragma once

    #include<iostream>
    #include<tabcpp/tabcpp.hpp>

    typedef enum 
    {
        COLOUR_RED, COLOUR_GREEN, COLOUR_BLUE,
        COLOUR_YELLOW, COLOUR_PINK, COLOUR_PURPLE,
        COLOUR_ORANGE, COLOUR_OTHER
    } Colour; //yes, I'm British

    //TABLE_BEGIN People
    //TABLE_END People

#### include/example/people_table.py

    from tabcpp import *

    tables = [
            {
                'name': 'People',
                'fields': [
                    field('std::string', 'name'), 
                    field('int', 'age'),
                    field('float', 'height'),
                    field('Colour', 'favouriteColour')
                ],
                'key': key('auto', 'short', 'id')
            }
    ]

#### src/example.cpp

    #include<example/example.hpp>

    #include<tabcpp/tabcpp.hpp>

    int main()
    {
        //initialise an empty table
        People people;
        //adding a row to the table
        people.add("Jenifer", 32, 1.6, COLOUR_GREEN);
        //adding a row and getting its unique (automatically generated) key
        short john_id = people.add("John", 22, 1.8, COLOUR_BLUE);
        //giving the key a name for access convenience
        people.makeLabel(john_id, "JOHN");
        people.add("Harold", 69, 1.7, COLOUR_PURPLE);
        //getting data via a label
        float john_height = people.height.get(people.labels["JOHN"]); 
        std::cout << "John's height is " << john_height << " metres" << std::endl; 
        return 0;
    }
        
#### Build Commands

    $ tabcpp.sh load include/example example.hpp people_table
    $ g++ -Iinclude src/example.cpp -o example 

## Other Options and Disclaimer
This implementation is not the only option for tables in C++.
A cursory search will turn up something like [uthash](https://github.com/troydhanson/uthash), and so this project does not have much of a claim to originality.
Tabular-C++ however likes to centre its data on column vectors as opposed to row structs, a design choice which arose from the personal taste of the author. 
This choice should favour operations on successive column elements, but might suffer with operations involving elements in the same row.  
It is also notable that Tabular-C++ favours class methods to macros in its usage (neglecting actual table construction. 
 
## Help

I welcome posts in this repository's Issues section. 
The toolset is very young and already has undergone some major design changes, so there are bound to be some teething issues. 

