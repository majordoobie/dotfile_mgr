-- File sets all the set configs

-- set variable nnoremap to the bind function specified in keymap
local nnoremap = require('majordoobie.keymap').nnoremap

-- Set numbers
vim.opt.nu = true
vim.opt.relativenumber = true

-- keep buffer alive in the background
vim.opt.hidden = true
vim.opt.errorbells = false

-- Set the tab settings
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.smartindent = true

-- Fix how highlighitng works
vim.opt.incsearch = true
vim.opt.hlsearch = true
vim.opt.wrap = false
nnoremap("<CR>", ":noh<CR><CR>")

-- Set how undo works
vim.opt.swapfile = false
vim.opt.backup = false
vim.opt.undodir = os.getenv("HOME") .. "/.vim/undodir"
vim.opt.undofile = true

-- Set colums
vim.opt.signcolumn = "yes"
vim.opt.colorcolumn = "80"

-- misc
vim.opt.scrolloff = 20
vim.opt.updatetime = 50
vim.opt.winheight = 50
vim.opt.showmatch = true    -- Allow seeing matching brackets
vim.opt.showcmd = true      -- Show the command used but could slow down terminal
vim.opt.showmode = true     -- show the current mode you are in

-- Don't pass messages to |ins-completion-menu|.
vim.opt.shortmess:append("c")

-- Give more space for displaying messages.
vim.opt.cmdheight = 1
vim.opt.termguicolors = true
vim.opt.isfname:append("@-@")

-- set leader key to space
vim.g.mapleader = " "

-- Set the colorscheme
vim.cmd "colorscheme gruvbox"
vim.opt.background = "dark"
 
