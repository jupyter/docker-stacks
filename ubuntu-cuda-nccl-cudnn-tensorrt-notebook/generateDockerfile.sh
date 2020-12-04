#!/bin/bash

tmpFile=./tmp

> $tmpFile

cat ../base-notebook/Dockerfile >> $tmpFile
cat ../minimal-notebook/Dockerfile >> $tmpFile
cat ../scipy-notebook/Dockerfile >> $tmpFile

sed -i 's/ARG ROOT_CONTAINER/# &/g' $tmpFile
sed -i 's/ARG BASE_CONTAINER/# &/g' $tmpFile
sed -i 's/FROM $BASE_CONTAINER/# &/g' $tmpFile
sed -i 's/ARG NB_USER/# &/g' $tmpFile

cat base.Dockerfile > Dockerfile
cat $tmpFile >> Dockerfile
cat tensorrt.Dockerfile >> Dockerfile

rm $tmpFile