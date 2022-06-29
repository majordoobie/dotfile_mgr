local Remap = require("majordoobie.keymap")
local nnoremap = Remap.nnoremap

nnoremap("<C-f>", function()
    require('telescope.builtin').grep_string({ search = vim.fn.input("Grep For > ")})
end)
nnoremap("<Leader>gf", function()
    require('telescope.builtin').find_files()
end)
nnoremap("<leader>vh", function()
    require('telescope.builtin').man_pages({sections = {"ALL"}})
end)
