-- Turn off markdownlint globally. LazyVim's markdown extra wires
-- markdownlint-cli2 through nvim-lint (diagnostics) and conform (fix).
return {
  {
    "mfussenegger/nvim-lint",
    opts = function(_, opts)
      opts.linters_by_ft = opts.linters_by_ft or {}
      opts.linters_by_ft.markdown = {}
      opts.linters = opts.linters or {}
      opts.linters.markdownlint = { condition = function() return false end }
      opts.linters["markdownlint-cli2"] = { condition = function() return false end }
    end,
  },
  {
    "stevearc/conform.nvim",
    optional = true,
    opts = function(_, opts)
      opts.formatters_by_ft = opts.formatters_by_ft or {}
      for _, ft in ipairs({ "markdown", "markdown.mdx" }) do
        local formatters = opts.formatters_by_ft[ft]
        if formatters then
          opts.formatters_by_ft[ft] = vim.tbl_filter(function(name)
            return name ~= "markdownlint-cli2" and name ~= "markdownlint"
          end, formatters)
        end
      end
    end,
  },
}
