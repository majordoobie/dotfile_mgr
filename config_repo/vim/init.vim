" curl curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
" This uses the plug manager for managing plug-ins. The following call will
" make sure that the file is called.



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

" set the theme
colorscheme gruvbox

" Set leader
let mapleader=" "

"""""""""""""""""""""""""""""""""""""""""""""""""""" Buffer settings
set clipboard+=unnamed

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

