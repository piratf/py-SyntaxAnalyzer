cd ../LexicalAnalyzer
make run
cd -
ls
cp ../LexicalAnalyzer/result.txt . -f
python3 main.py
subl output.txt
