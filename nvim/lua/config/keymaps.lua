-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

vim.keymap.set("t", "<Esc><Esc>", "<C-\\><C-n>", { desc = "Enter Normal Mode" })

-- Pick a spelling correction for the word under the cursor. LazyVim only maps
-- the spell toggle (<leader>us); the built-ins below still work unmapped.
vim.keymap.set("n", "<leader>zs", function()
  Snacks.picker.spelling()
end, { desc = "Spelling suggestions" })
