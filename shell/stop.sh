#!/bin/sh
for ii in `ps auxf|grep "example_hsync"|grep -v grep|awk '{print $2}'`; do kill -9 ${ii}; done
