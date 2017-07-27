for i in Q W E R T Y U I O P A S D F G J K L Z X C V B N M Number
do
  python gameBoomersDownloader.py $i
  python ../parser/parser.py texts/verbs$i >commands/verbs$i
done
