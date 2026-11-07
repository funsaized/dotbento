return {
  {
    "blackhat-7/vellum.nvim",
    ft = "markdown",
    cmd = "Vellum",
    keys = {
      { "<leader>mp", "<cmd>Vellum<cr>", desc = "Markdown preview" },
      {
        "<leader>mz",
        function()
          require("vellum").zoom()
        end,
        desc = "Zoom Markdown image",
      },
    },
    opts = {},
    config = function(_, opts)
      local vellum = require("vellum")
      vellum.setup(opts)

      -- Vellum hardcodes a right split; move it beside the source on the left.
      local open = vellum.open
      vellum.open = function()
        local source_win = vim.api.nvim_get_current_win()
        open()
        local preview_win = vim.fn.bufwinid("vellum://preview")
        if preview_win ~= -1 and preview_win ~= source_win then
          vim.api.nvim_win_set_config(preview_win, { split = "left", win = source_win })
        end
      end
    end,
  },
}
