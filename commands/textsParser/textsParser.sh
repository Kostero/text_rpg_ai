for game in `ls texts`
do
  echo $game
  python textsParser.py texts/$game >> parsedCommands.txt
done
