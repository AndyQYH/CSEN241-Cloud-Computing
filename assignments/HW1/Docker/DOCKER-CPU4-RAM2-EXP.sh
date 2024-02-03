declare -a test_cpu=("20000" "40000")
declare -a test_memory=("1G" "2G")
declare -a test_file=("seqrd" "rndrd")
max_time=20
iterations=5

#get cpu / ram info and use that as the output file name
total_ram(){
	local totalram=$(cat /proc/meminfo | grep -i 'memtotal' | grep -o '[[:digit:]]*')
	echo "$totalram"
}

total_cpu(){
	local totalcpu=$(lscpu | grep -e '^CPU(s)' | grep -o '[[:digit:]]*')
	echo "$totalcpu"
}

print_section(){
	printf %"$(tput cols)"s | tr " " "-" >> "$1"
	printf "\n" >> "$1"
	printf %"$(tput cols)"s | tr " " "-" >> "$1"
	printf "\n" >> "$1"
}


#Variables for identifying system specs and test output file
rams=$(total_ram)
cpus=$(total_cpu)
echo "rams: $rams kb"
echo "cpus: $cpus"
file_to_write="results/DOCKER_CPU${cpus}_RAM${rams}.txt"
echo "file will be written to $file_to_write ..."
# end

echo "$file_to_write" > "$file_to_write"
print_section "$file_to_write"
#test cases for cpu
#<<com
echo "Now Started Testing CPU ..."
echo -e "Now Started Testing CPU ... \n" >> "$file_to_write"
print_section "$file_to_write"

for i in "${test_cpu[@]}"
do
	for ((j=1; j<="$iterations"; j++))
	do
		echo "iteration $j ..."
		sysbench --test=cpu --cpu-max-prime="$i" --time="$max_time" run >> "$file_to_write"
		printf %"$(tput cols)"s | tr " " "-" >> "$file_to_write"
		printf "\n\n" >> "$file_to_write"
	done
done
#com

print_section "$file_to_write"

#<<com
#test cases for memory
echo "Now Started Testing RAM ..."
echo -e "Now Started Testing RAM ... \n" >> "$file_to_write"
print_section "$file_to_write"

for k in "${test_memory[@]}"
do
	for ((l=1; l<="$iterations"; l++))
	do
		echo "iteration $l ..."
		sysbench --test=memory --memory-block-size="$k" run >> "$file_to_write"
		printf %"$(tput cols)"s | tr " " "-" >> "$file_to_write"
		printf "\n\n" >> "$file_to_write"
	done
done
#com

print_section "$file_to_write"

#<<com
#test cases for fileio
#needs to refresh cache every run to make sure fairness
echo "Now Started Testing FileIO ... \n"
echo -e "Now Started Testing FileIO ... \n" >> "$file_to_write"
print_section "$file_to_write"

sysbench --test=fileio cleanup
sysbench --test=fileio prepare
for m in "${test_file[@]}"
do
	#sysbench --test=fileio --file-test-mode="$m" --time="$max_time" prepare
	for ((n=1; n<="$iterations"; n++))
	do
		echo "iteration $n ..."
		sysbench --test=fileio --file-test-mode="$m" --time="$max_time" run >> "$file_to_write"
		echo "$n test done for $m ..."
		echo "please perform host cache drop right now  ..."
		sleep 5
		printf %"$(tput cols)"s | tr " " "-" >> "$file_to_write"
		printf "\n\n" >> "$file_to_write"
	done
	#sysbench --test=fileio --file-test-mode="$m" --time="$max_time" cleanup
done
sysbench --test=fileio cleanup
#com
