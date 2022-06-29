-- This file is executed after everything else is loaded
local Remap = require("majordoobie.keymap")
local nnoremap = Remap.nnoremap
local vnoremap = Remap.vnoremap
local nmap = Remap.nmap
local vmap = Remap.vmap

-- Disable V + k and V + j; they get in the way when moving quickly
vmap("<S-k>", "<Nop>")
vmap("<S-j>", "<Nop>")

-- Open netRW
nnoremap("gf", ":Ex<CR>")

-- Change the ^ and $ to easier to type keys
nmap("gh", "^")
nmap("gl", "$")

-- Update how indentation works
vnoremap("<", "<gv")
vnoremap(">", ">gv")
 
-- Modify Copy and paste
vnoremap("<leader>p", "\"+p")   -- Paste from global buffer
nnoremap("<leader>p", "\"+p")   -- Paste from global buffer

vnoremap("<leader>y", "\"+y")   -- Copy into global buffer
nnoremap("<leader>y", "\"+y")   -- Copy into global buffer

vnoremap("<leader>d", "\"_d")   -- Delete without affecting the unamged buffer
nnoremap("<leader>d", "\"_d")   -- Delete without affecting the unamed buffer

vnoremap("x", "\"_x")           -- Delete without affecting the unamged buffer
nnoremap("x", "\"_x")           -- Delete without affecting the unamed buffer

vnoremap("r", "\"_r")           -- Delete without affecting the unamged buffer
nnoremap("r", "\"_r")           -- Delete without affecting the unamed buffer


