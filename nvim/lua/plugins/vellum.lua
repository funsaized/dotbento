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
  },
}
