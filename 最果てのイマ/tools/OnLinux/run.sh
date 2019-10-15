for line in `cat file.txt`
do
echo $line
./exbip bip/$line $line.txt
done
