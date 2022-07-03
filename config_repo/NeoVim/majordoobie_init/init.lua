print("inside majordoobie/init")
require("majordoobie.set")

-- Open file in current window
vim.g.netrw_browse_split = 0
-- remove banner
vim.g.netrw_banner = 0
-- show tree like structure
vim.g.netrw_liststyle = 3
-- Set width of window to 25%
vim.g.netrw_winsize = 25
