attempt_counter=0
max_attempts=$1

echo "Attempting to login to foundations."
until $(foundations login http://localhost:5558 -u test -p test >> /dev/null); do
  if [ ${attempt_counter} -eq ${max_attempts} ];then
    echo "Max attempts reached"
    exit 1
  fi

  printf '.'
  attempt_counter=$(($attempt_counter+1))
  sleep 2
done

attempt_counter=0

cd ~/orbit_install/test/
echo "Attempting to create a monitor."
until $(foundations monitor create . main.py >> /dev/null); do
  if [ ${attempt_counter} -eq ${max_attempts} ];then
    echo "Max attempts reached"
    exit 1
  fi

  printf '.'
  attempt_counter=$(($attempt_counter+1))
  sleep 2
done

echo "Able to create monitor"
