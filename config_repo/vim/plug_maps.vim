" telescope commands
nnoremap <leader>ps :lua require('telescope.builtin').grep_string({ search = vim.fn.input("Grep For > ")})<CR>
nnoremap <leader>gf <cmd>Telescope find_files<cr>
nnoremap <leader>fg <cmd>Telescope live_grep<cr>
nnoremap <leader>fb <cmd>Telescope buffers<cr>
nnoremap <leader>fh <cmd>Telescope help_tags<cr>
nnoremap <leader>fm <cmd>Telescope man_pages<cr>

" GoTo code navigation.
nmap <silent> jd <Plug>(coc-definition)
nmap <silent> vp <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> vu <Plug>(coc-references)
nnoremap <silent> K :call ShowDocumentation()<CR>


" Nerd tree 
nnoremap gf :NERDTreeToggle<CR>
