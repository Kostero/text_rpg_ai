mkdir $2
./text.sh $1 >$2/texts.txt
./items.sh $1 >$2/items.txt
./rooms.sh $1 >$2/rooms.txt
./objects.sh $1 >$2/objects.txt
