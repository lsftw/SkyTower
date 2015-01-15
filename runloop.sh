while [ 1 ]
do
	clear
	python skytower/game.py
	echo [Enter] to re-run. Any other input exits.
	read input
	if [ ${#input} != 0 ]
	then
		break
	fi
done