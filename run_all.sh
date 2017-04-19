for file in `cat $1`
do
	python golovinAgent.py $file gamesDownloader/games/
done
