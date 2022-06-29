-- This file has all the plugins installed and managed by the packer module

-- This code is from the packer page. It is a bootstrap to automatically clone
-- the packer git so that it is available on any machine you are setting up
local fn = vim.fn
local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
if fn.empty(fn.glob(install_path)) > 0 then
  packer_bootstrap = fn.system({'git', 'clone', '--depth', '1', 'https://github.com/wbthomason/packer.nvim', install_path})
end

-- Plugins go here
return require('packer').startup(function()
    -- Packer can manage itself
    use 'wbthomason/packer.nvim'

    -- Color scheme
    use "ellisonleao/gruvbox.nvim"

    -- telescope requirements (checkhealth telescope)
    use("nvim-lua/plenary.nvim")
    use("nvim-lua/popup.nvim")
    use("nvim-telescope/telescope.nvim")
    use("nvim-treesitter/nvim-treesitter", {
        run = ":TSUpdate"
    })

    -- Multi selection
    -- https://github.com/mg979/vim-visual-multi/wiki/Mappings
    use("mg979/vim-visual-multi")

    -- runs the boot strap if the variable exists (if git was cloned)
    if packer_bootstrap then
        require('packer').sync()
    end
end)
