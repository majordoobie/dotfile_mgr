" curl curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
" This uses the plug manager for managing plug-ins. The following call will
" make sure that the file is called.

set nocompatible		" be iMproved, required
filetype off		        " required

call plug#begin('~/.config/nvim/plugged')  	" this stores all the plugins downloaded

Plug 'morhetz/gruvbox'		        	" Installs the theme
Plug 'tpope/vim-fugitive'			" Git wrapper
Plug 'preservim/nerdtree'			" File explorer
Plug 'ctrlpvim/ctrlp.vim' 			" Fuzzy for finding files with ctrl-p
Plug 'neoclide/coc.nvim', {'branch': 'release'}	" syntax highlighting

call plug#end()	" Above is where all the plug commands go

colorscheme gruvbox				" set the theme
map <silent> <C-n> :NERDTreeFocus<CR>		" Set the nerd tree focus to ctrl + n use :q to exit it

