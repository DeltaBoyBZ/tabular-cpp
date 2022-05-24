#pragma once
#include<iostream>
#include<tabcpp/tabcpp.hpp>

typedef enum 
{
    COLOUR_RED, COLOUR_GREEN, COLOUR_BLUE,
    COLOUR_YELLOW, COLOUR_PINK, COLOUR_PURPLE,
    COLOUR_ORANGE, COLOUR_OTHER
} Colour;

//TABLE_BEGIN People
TABCPP_TABLE(People, short, TABCPP_CONSTRUCTOR(People, id, short)
, TABCPP_DESTRUCTOR(People)
, TABCPP_FIELD(short, std::string, name);
TABCPP_FIELD(short, int, age);
TABCPP_FIELD(short, float, height);
TABCPP_FIELD(short, Colour, favouriteColour);
TABCPP_FIELD(short, short, id);
, TABCPP_ADD_FUNC_AUTO(short, TABCPP_ARGS(std::string name, int age, float height, Colour favouriteColour), TABCPP_APPEND(name, name);
TABCPP_APPEND(age, age);
TABCPP_APPEND(height, height);
TABCPP_APPEND(favouriteColour, favouriteColour);
);
, TABCPP_REMOVE_FUNC(short, TABCPP_REMOVE(name, index);
TABCPP_REMOVE(age, index);
TABCPP_REMOVE(height, index);
TABCPP_REMOVE(favouriteColour, index);
TABCPP_REMOVE(id, index);
);
);
//TABLE_END People

#include"example_tables.hpp"

/*TABCPP_OPEN
from tabcpp import * 
tables = [
    {
        'name': 'Points',
        'fields': [
            field('float', 'x'),
            field('float', 'y')
        ],
        'key': key('auto', 'int', 'id')
    }
]
TABCPP_CLOSE*/
