git clone https://github.com/danielricks/textplayer.git
cd textplayer
git clone https://github.com/DavidGriffith/frotz.git
cd frotz
make dumb
cd ../..
pip install -r requirements.txt
# install nltk data
python -m nltk.downloader punkt
git clone https://github.com/emilmont/pyStatParser.git
cd pyStatParser
python setup.py install --user
cd ..
