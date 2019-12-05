#!/bin/bash

echo_err () {
    echo -e "\n$1\n" 1>&2
    exit 1
}

docker=$(which docker)

check_docker () {
    if [[ -z "${docker}" ]]
    then
        echo_err "Please, install Docker."
    fi
}

get_args() {
    if [[ $# -ne 2 ]]
    then
        echo_err "USAGE: $0 <path_to_decryption_key_file> <remote_redis_host>"
    else
        path_to_decryption_key=$(realpath $1)
        remote_redis_host=$2
    fi
}

check_key () {
    if [[ ! -f "${path_to_decryption_key}" ]]
    then
        echo_err "Decryption key file not found. Please, provide the correct path to a decryption key file."
    fi
}

check_not_url () {
    if echo ${remote_redis_host} | grep -q '^redis://'
    then
        echo_err "Please, provide the remote Redis host using the format host:port (port optional, defaults to 6379).\nDo not specify protocol like when specifying URLs."
    fi
}

check_not_localhost () {
    if echo ${remote_redis_host} | grep -q '^localhost' || echo ${remote_redis_host} | grep -q '^127.0.0.1'
    then
        echo_err "This utility is intended to be used as a proxy for remote encrypted Redis connections."
    fi
}

get_listen_port () {
    if [[ -z "${redis_gateway_listen_port}" ]]
    then
        redis_gateway_listen_port=6379
    fi
}

format_remote_host () {
    redis_host=$1
    host=$(echo ${remote_redis_host} | cut -d ':' -f 1)
    port=$(echo ${remote_redis_host} | cut -d ':' -f 2)
    if [[ "${host}" = "${port}" ]]
    then
        port=6379
    fi
    ip_address=$(echo $host | grep -E '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
    if [[ -n "${ip_address}" ]];
    then
        remote_redis_host="[${ip_address}]:${port}"
    else
        remote_redis_host="${host}:${port}"
    fi

}

run_docker() {
    ${docker} run --rm -d \
        -v ${path_to_decryption_key}:/spiped/key:ro \
        -p 127.0.0.1:${redis_gateway_listen_port}:${redis_gateway_listen_port} \
        --name local-redis-gateway \
        --init spiped:1.6 -e -s "[0.0.0.0]:${redis_gateway_listen_port}" -t "${remote_redis_host}" 1>/dev/null
}

inform_user_if_docker_running () {
    if [[ $? -eq 0 ]]
    then
        echo -e "\nYour local Redis gateway is running at 127.0.0.1:${redis_gateway_listen_port}. Set your REDIS_URL to redis://127.0.0.1:${redis_gateway_listen_port}.\n"
    fi
}

check_docker
get_args $@
check_key
check_not_url
check_not_localhost
get_listen_port
format_remote_host
run_docker
inform_user_if_docker_running
