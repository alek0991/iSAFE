#!/bin/bash
isafe=../src/isafe.py
input=./demo.txt
output=./demo #the program adds .isafe.out to it
$isafe -h
$isafe $input $output
