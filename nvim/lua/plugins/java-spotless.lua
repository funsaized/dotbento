-- jdtls format off; Spotless (Palantir) owns Java when the module pom has it.
local function pom_root()
  return vim.fs.root(0, { "pom.xml" })
end

local function pom_has_spotless(root)
  local f = io.open(root .. "/pom.xml", "r")
  if not f then
    return false
  end
  local text = f:read("*a")
  f:close()
  return text:find("spotless-maven-plugin", 1, true) ~= nil
end

return {
  {
    "mfussenegger/nvim-jdtls",
    optional = true,
    opts = function(_, opts)
      opts.settings = opts.settings or {}
      opts.settings.java = vim.tbl_deep_extend("force", opts.settings.java or {}, {
        format = { enabled = false },
      })
    end,
  },
  {
    "stevearc/conform.nvim",
    optional = true,
    opts = function(_, opts)
      opts.formatters_by_ft = opts.formatters_by_ft or {}
      opts.formatters_by_ft.java = { "spotless_maven" }
      opts.formatters = opts.formatters or {}
      opts.formatters.spotless_maven = {
        stdin = false,
        condition = function()
          local root = pom_root()
          return root ~= nil and pom_has_spotless(root)
        end,
        cwd = function()
          return pom_root()
        end,
        command = function()
          local root = pom_root()
          if root and vim.uv.fs_stat(root .. "/mvnw") then
            return root .. "/mvnw"
          end
          return "mvn"
        end,
        args = function(_, ctx)
          return { "-q", "spotless:apply", "-DspotlessFiles=\\Q" .. ctx.filename .. "\\E" }
        end,
      }
    end,
  },
}
