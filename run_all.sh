for file in `cat $1`
do
	python golovinRunner.py $file --path=gamesDownloader/games/ --quiet --steps=$2
done
