Install `perl` before launching `env.sh` (`sudo apt-get install perl`).

### Commands

* `./ztools731/txd game.z5 >fullGame.txt` - decompiles the whole game
* `./ztools731/infodump -g game.z5 >routines.txt` - prints all routines from game
* `./general.sh text game.z5 >gameText.txt` - creates file with all texts in game.
* `./general.sh items game.z5 >items.txt`
* `./general.sh objects game.z5 >objects.txt`
* `./general.sh rooms game.z5 >rooms.txt`
* `./general.sh words game.z5 >words.txt` - prints all words from dictionary
* `./all.sh game.z5 folder` - creates `folder` directory for game
  and creates files with everything mentioned above.

### Note

Do not worry about following warning during runs:
```
Possible precedence issue with control flow operator
at /usr/local/share/perl/5.22.1/Games/Rezrov/Speech.pm line 287, <DATA> line 259.
```
