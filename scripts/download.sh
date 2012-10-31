#!/usr/bin/env bash

function color_echo() {
	echo -e "\e[1;33m$@\e[0m"
}

bundle_path=~/.vim/bundle
mkdir -p $bundle_path
cd $bundle_path

if [ ! -d "bufexplorer.git" ]; then
	color_echo "Downloading bufexplorer.git"
	git clone --depth 1 git://github.com/corntrace/bufexplorer.git
fi

if [ ! -d "genutils.git" ]; then
	color_echo "Downloading genutils.git"
	git clone --depth 1 git://github.com/vim-scripts/genutils.git
fi

if [ ! -d "lookupfile.git" ]; then
	color_echo "Downloading lookupfile.git"
	git clone --depth 1 git://github.com/vim-scripts/lookupfile.git
fi

if [ ! -d "nerdtree.git" ]; then
	color_echo "Downloading nerdtree.git"
	git clone --depth 1 git://github.com/vim-scripts/The-NERD-tree.git
fi

if [ ! -d "taglist.git" ]; then
	color_echo "Downloading taglist.git"
	git clone --depth 1 git://github.com/vim-scripts/taglist.vim.git
fi
