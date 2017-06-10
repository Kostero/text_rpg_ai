./gDriveDownloader.sh 0B3lpCS07rg43bVBmd1lSVUVSb28 scholar_required_files.zip
./gDriveDownloader.sh 0B7XkCwpI5KDYNlNUTTlSS21pQmM GoogleNews-vectors-negative300.bin.gz
gunzip GoogleNews-vectors-negative300.bin.gz
mv GoogleNews-vectors-negative300.bin.gz ../word2vec/
unzip scholar_required_files.zip
mv postagged_wikipedia_for_word2vec.bin ../word2vec/
rm post* scholar_required_files.zip 


