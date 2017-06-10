mkdir commands objects
for game in `ls games`
do
  echo $game
  timeout 10s ./ztools731/infodump -g games/$game >commands/$game.txt 2>/dev/null
  timeout 10s ./general.sh items games/$game >items/$game.txt 2>/dev/null
  if ! [[ -s commands/$game.txt ]]
  then
    rm commands/$game.txt
  fi
  if ! [[ -s items/$game.txt ]]
  then
    rm items/$game.txt
  fi
done
