mkdir $2
./text.sh $1 >$2/texts.txt
./items.sh $1 >$2/items.txt
./rooms.sh $1 >$2/rooms.txt
./objects.sh $1 >$2/objects.txt
./words.sh $1 >$2/words.txt
./ztools731/txd $1 >$2/fullgame.txt
./ztools731/infodump -g $1 >$2/routines.txt
