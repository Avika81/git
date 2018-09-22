all: debugging running

debugging:
	> output_debugging.txt
	time python3 testing.py 1 1 1>> output_debugging.txt

running:
	> output_running.txt
	time python3 testing.py 0 0 0 >> output_running.txt
	sort  -g -k 2 -o output_running.txt output_running.txt  # sorts the file according to the shift id
	sed -i '1s/^/[/' output_running.txt  # insert a '[' at the start of the file
	sed -i 's/ //g' output_running.txt  # remove all blank spaces
	echo "]" >> output_running.txt
update:
	ssh avi@146.148.80.14 './scheduler-update.sh'
