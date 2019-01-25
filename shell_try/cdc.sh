#!/bin/bash  
cd ../CDC/THUMOS14/train/img/

c=0
for file in $(ls)
do
  allcls[$c]=$file
  ((c++))
done

echo ${#allcls[@]}
cd ~/data/C3D/UCF101_frm

for cls in ${allcls[@]}
do
  echo $cls
  echo -----------outer------------------
  for file1 in $(ls -F | find -type d -name "*$cls*")
  do
    echo $file1
    echo ------inner-----------
    cp -r $file1 ../../CDC/THUMOS14/train/img/
  done
done

rm -r *SkyDiving*/*
