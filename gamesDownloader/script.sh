wget ftp://ftp.funet.fi/pub/misc/ifarchive/games/zcode/*
for i in `ls *.zip`; do yes | unzip $i; done
mkdir games
mv */*.{z,Z}{1,2,3,4,5,6,7,8,9,blorb} games/
mv *.{z,Z}{1,2,3,4,5,6,7,8,9,blorb} games/
find . -maxdepth 1 -type f ! -name 'script.sh' -delete
find . -type d ! -name 'games' -delete
