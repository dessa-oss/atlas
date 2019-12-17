attempt_counter=0
max_attempts=$1

until $(foundations submit scheduler . main.py); do
    if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Max attempts reached"
      exit 1
    fi

    printf '.'
    attempt_counter=$(($attempt_counter+1))
    sleep 1
done

echo "Able to submit job"