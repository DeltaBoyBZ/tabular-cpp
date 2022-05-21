# create new environment variable for Tabular-C++ root
echo "export TABCPP_ROOT=$(pwd)" >> ~/.bashrc

# add root to PATH
echo 'export PATH=${PATH}:'"$(pwd)" >> ~/.bashrc

# add root to include path
echo 'export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}:'"$(pwd)/include" >> ~/.bashrc

