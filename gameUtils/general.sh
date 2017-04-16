./empty.sh $2 >tmpemp
rezrov $2 -cheat -rows 25 -column 80 -playback $1.txt -test >tmpinp
python3 clean.py tmpemp tmpinp
rm tmpemp tmpinp
