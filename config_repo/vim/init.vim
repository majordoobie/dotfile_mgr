" curl curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
" This uses the plug manager for managing plug-ins. The following call will
" make sure that the file is called.

""""""""""""""""""""""""""""""" Sets
" Fix Tabs
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set smartindent

" Set number column
set relativenumber
set number

" Fix the search highlight
set incsearch
set hlsearch
set wrapscan
set nowrap
highlight ColorColumn ctermbg=0 guibg=lightgrey
nnoremap <CR> :noh<CR><CR>

" Keep buffer alive in the background if you leave it
set hidden

" column add
set signcolumn=yes
set colorcolumn=80
set ruler

" Modify backup. Some LSP have issues with these backup strategies
set noerrorbells
set noswapfile
set nobackup

" misc
set scrolloff=15
set cmdheight=2
set clipboard+=unnamedplus
set updatetime=300

" Don't pass messages to complesion menu
set shortmess+=c

""""""""""""""""""""""""""""""" Plugins
call plug#begin('~/.config/nvim/autoload')  	" this stores all the plugins downloaded
Plug 'gruvbox-community/gruvbox'
Plug 'preservim/nerdtree'

" Native LSP
Plug 'neovim/nvim-lspconfig'

" Both needed for telescope
Plug 'nvim-telescope/telescope.nvim'
Plug 'nvim-lua/plenary.nvim'

" CoC
Plug 'neoclide/coc.nvim', {'branch': 'release'}

call plug#end()	" Above is where all the plug commands go

""""""""""""""""""""""""""""""" Mappings
" set the theme
colorscheme gruvbox

" Set leader
let mapleader=" "

" Place x and r into black hole instead of the unnamed registers to forget
" them
nnoremap x "_x
nnoremap r "_r
nnoremap <leader>d "_d
vnoremap <leader>d "_d

" Copy and paste from global clipboard
nnoremap yy "+yy
vnoremap y "+y

nnoremap p "+p
vnoremap p "+p
nnoremap P "+P
vnoremap P "+P


" Map the indentation to work with the group indentation
vnoremap < <gv
vnoremap > >gv

"^$ The symbol is too hard to press
map gh ^
map gl $

