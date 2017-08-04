#!/bin/bash

basepath=$(cd `dirname $0`; pwd)
home=~
configfile=ipcluster_config.py
line=--------------------------

function create()
{
    for profile in $@
    do
        echo ${line}
        echo "start create ${profile}"
        ipython profile create --parallel --profile=${profile}
	dst="${home}/.ipython/profile_${profile}/${configfile}"
        echo "copy config file to ${dst}"
        cp -f ${basepath}/${configfile} ${dst}
    done
}

while getopts f: OPTION
do
    case ${OPTION} in
        f)
            profiles=`cat ${OPTARG}`
            ;;
        \?)                     
            ;;
    esac
done

if [ -z "${profiles}" ]; then
    profiles=$@
fi

create ${profiles}
