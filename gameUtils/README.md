Install `perl` before launching `env.sh` (`sudo apt-get install perl`).

### Commands

* `./ztools731/txd game.z5 >fullGame.txt` - decompiles the whole game
* `./ztools731/infodump -g game.z5 >routines.txt` - prints all routines from game
* `./text.sh game.z5 >gameText.txt` - creates file with all texts in game.
* `./items.sh game.z5 >items.txt`
* `./objects.sh game.z5 >objects.txt`
* `./rooms.sh game.z5 >rooms.txt`
* `./words.sh game.z5 >words.txt` - prints all words from dictionary
* `./all.sh game.z5 folder` - creates `folder` directory for game
  and creates files with everything mentioned above.
