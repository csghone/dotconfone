#!/bin/bash

# Clone in VIM and symlink to NVIM
cd ~/.vim/bundle/
git clone https://github.com/Valloric/YouCompleteMe.git
git clone https://github.com/rdnetto/YCM-Generator.git

ln -s ~/.vim/bundle/YouCompleteMe/ ~/.config/nvim/bundle/
ln -s ~/.vim/bundle/YCM-Generator/ ~/.config/nvim/bundle/

# Get latest code
cd YouCompleteMe/
git submodule update --init --recursive

# Install using PYTHON3
sudo apt-get install python3-dev
python3 ./install.py --clang-completer
