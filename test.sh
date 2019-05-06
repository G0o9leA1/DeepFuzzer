# /bin/bash
bool="true"
for lib in afl-gcc afl-fuzz python3 clang clang-check cproto
do 
if ! hash $lib 2>/dev/null; then
  echo "Error: $lib is not installed." >&2
  bool="false"
  else
	echo "$lib Found!"
fi
done
if [ "$bool" = true ] ; then
    echo 'All Requirements Satisfied! '
	if [ ! -d "cache" ]; then
    	eval "mkdir cache"
	fi
	if [ ! -d "out" ]; then
        eval "mkdir out"
        fi

    else
	echo "Test Failed. Please install the missing library and run test script again!"
fi
