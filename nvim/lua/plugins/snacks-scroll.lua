return {
	"folke/snacks.nvim",
	opts = {
		scroll = {
			enabled = true,
			-- Avoid feeding animated scroll positions back into Vellum's sync.
			filter = function(buf)
				return vim.g.snacks_scroll ~= false
					and vim.b[buf].snacks_scroll ~= false
					and vim.bo[buf].buftype ~= "terminal"
					and vim.bo[buf].filetype ~= "markdown"
					and vim.api.nvim_buf_get_name(buf) ~= "vellum://preview"
			end,
		},
	},
}
