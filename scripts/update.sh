#!/bin/bash

function color_echo() {
    echo -e "\e[1;33m$@\e[0m"
}

bundle_path=~/.vim/bundle
cd $bundle_path

# git
for i in *.git; do
    cd $i
    color_echo "Updating $i"
    git pull
    cd ..
done

# hg
for i in *.hg; do
    cd $i
    color_echo "Updating $i"
    hg pull
    cd ..
done

# svn
for i in *.svn; do
    cd $i
    color_echo "Updating $i"
    svn update
    cd ..
done
