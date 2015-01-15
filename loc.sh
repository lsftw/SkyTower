# Print js files by lines of code

cd ./skytower
#( find . -name '*.py' -print0 | xargs -0 cat ) | wc -l
find . -name '*.py' -print0 | xargs -0 wc -l | sort
read -p "$*"