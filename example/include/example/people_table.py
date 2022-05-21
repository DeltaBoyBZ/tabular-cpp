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
