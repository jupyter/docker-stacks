#!/usr/bin/env bash

basepath=$(cd `dirname $0`; pwd)

while getopts :f OPTION
do
    case ${OPTION} in
        f)
            dir_str= ${OPTARG}
            ;;
        \?)                       #如果出现错误，则解析为?
            create "${OPTARG}";
            ;;
    esac
done

function create()
{
    for profile in $@
    do
        echo "start create ${profile}"
    done
}

