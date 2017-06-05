mkdir commands
for game in `ls games`
do
  echo $game
  timeout 10s ./ztools731/infodump -g games/$game >commands/$game.txt 2>/dev/null
  if ! [[ -s texts/$game.txt ]]
  then
    rm commands/$game.txt
  fi
done
