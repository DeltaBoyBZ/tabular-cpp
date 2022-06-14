# create new environment variable for Tabular-C++ root
echo "export TABCPP_ROOT=$(pwd)" >> ~/.bashrc

# add root to PATH
echo 'export PATH=${PATH}:${TABCPP_ROOT}' >> ~/.bashrc

# add root to include path
echo 'export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}:${TABCPP_ROOT}/include' >> ~/.bashrc

