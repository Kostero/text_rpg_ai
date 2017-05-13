for game in `cat textplayer/max_scores_selected.txt`
do
  if [[ $game == *".z5" ]]
  then
    python golovinRunner.py $game --quiet --steps=1000
  fi
done
