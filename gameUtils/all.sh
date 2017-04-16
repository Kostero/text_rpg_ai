mkdir $2
./general.sh text $1 >$2/texts.txt
./general.sh items $1 >$2/items.txt
./general.sh rooms $1 >$2/rooms.txt
./general.sh objects $1 >$2/objects.txt
./general.sh words $1 >$2/words.txt
./ztools731/txd $1 >$2/fullgame.txt
./ztools731/infodump -g $1 >$2/routines.txt
