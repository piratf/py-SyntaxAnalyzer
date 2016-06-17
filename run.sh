cd ../LexicalAnalyzer
make run
cd -
cp ../LexicalAnalyzer/result.txt ../LexicalAnalyzer/parseCode.txt ../LexicalAnalyzer/output.txt . -f
python3 main.py
subl output.txt
