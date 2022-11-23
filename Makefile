ifdef DEST
export: 
	cp tabcpp.sh tabcpp.py construct_table.py ${DEST}
	if [ ! -d "${DEST}/include/tabcpp" ] ; then mkdir ${DEST}/include/tabcpp ; fi 
	cp -r include/tabcpp ${DEST}/include
endif

