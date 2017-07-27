rm parsedCommands.txt
for game in `ls texts`
do
  echo $game
  python ../parser/parser.py texts/$game >> parsedCommands.txt
done
