./run1.sh $1 0
./minisat $1.satinput $1.satoutput
./run2.sh $1 1
