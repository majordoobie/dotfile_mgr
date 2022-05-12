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

filetype plugin indent on
syntax on
set ruler                       " Show the line and column numbers of the cursor.

set colorcolumn=80				" set visual line length
" set textwidth=80                " Hard-wrap long lines as you type them.

set background=dark
highlight ColorColumn ctermbg=0 guibg=lightgrey
set number
set smartcase
set hlsearch
set noerrorbells
set tabstop=4 softtabstop=4
set expandtab
set smartindent


