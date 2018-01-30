#!/bin/bash
# this shell scrip is to reset something

echo -e "remove the weblist.txt file"

rm weblist.txt

echo -e "remove the temp page* file "

rm ./page_file/page*

rm sensitive_data_of_phone.txt sensitive_data_of_id.txt

echo -e "Everthing is OK!"
