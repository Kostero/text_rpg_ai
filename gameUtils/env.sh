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
