for game in `ls textplayer/games`
do
  python golovinRunner.py $game --quiet --steps=1000
done
tail -n 50 scores | python getResult.py
