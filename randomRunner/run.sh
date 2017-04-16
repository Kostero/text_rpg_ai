mkdir $2
cd ../gameUtils
./ztools731/infodump -g $1 >../randomRunner/$2/routines.txt
./general.sh words $1 >../randomRunner/$2/words.txt
cd ../randomRunner
python commandsGenerator.py $2/routines.txt $2/words.txt $2/commands.txt
