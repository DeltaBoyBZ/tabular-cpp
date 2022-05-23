#pragma once
TABCPP_TABLE(Points, int, TABCPP_CONSTRUCTOR(Points, id, int)
, TABCPP_DESTRUCTOR(Points)
, TABCPP_FIELD(int, float, x);
TABCPP_FIELD(int, float, y);
TABCPP_FIELD(int, int, id);
, TABCPP_ADD_FUNC_AUTO(int, TABCPP_ARGS(float x, float y), TABCPP_APPEND(x, x);
TABCPP_APPEND(y, y);
);
, TABCPP_REMOVE_FUNC(int, TABCPP_REMOVE(x, index);
TABCPP_REMOVE(y, index);
TABCPP_REMOVE(id, index);
);
);
