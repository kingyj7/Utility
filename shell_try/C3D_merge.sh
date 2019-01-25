#!/bin/bash  
cd UCF101_frm1

c=0
for file in $(ls)
do
  allcls[$c]=$file
  ((c++))
done

echo ${#allcls[@]}
cd ../UCF101_frm

for cls in ${allcls[@]}
do
  echo $cls
  echo -----------outer------------------
  for file1 in $(ls -F | find -type d -name "*$cls*")
  do
    echo $file1
    echo ------inner-----------
    cp -r $file1 ../UCF101_frm1/$cls/
  done
done
