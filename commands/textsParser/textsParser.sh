for game in `ls texts`
do
  python textsParser.py $game >> parsedCommands.txt
done
