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
