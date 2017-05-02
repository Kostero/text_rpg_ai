mkdir texts
for game in `ls games`
do
  echo $game
  timeout 10s ./general.sh text games/$game >texts/$game.txt 2>/dev/null
  if ! [[ -s texts/$game.txt ]]
  then
    rm texts/$game.txt
  fi
done
