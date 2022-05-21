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

