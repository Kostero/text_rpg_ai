wget http://mirror.ifarchive.org/if-archive/infocom/tools/ztools/ztools731.tar.gz
mkdir ztools731/
tar -xvzf ztools731.tar.gz -C ztools731/
make -C ztools731/ all
wget http://edmonson.paunix.org/rezrov/Games-Rezrov-0.20.zip
unzip Games-Rezrov-0.20.zip
cd Games-Rezrov-0.20/
perl Makefile.PL
make
make test
sudo make install
cd ..
chmod +x *.sh
./all.sh Games-Rezrov-0.20/minizork.z3 minizork-example/
./ztools731/txd Games-Rezrov-0.20/minizork.z3 >minizork-example/fullgame.txt
