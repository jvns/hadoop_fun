for i in `cat NAMENODES`; do 
	scp bytesum $i
	ssh $i "killall bytesum"
	ssh $i "nohup ./bytesum"
done
