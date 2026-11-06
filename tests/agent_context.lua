vim.opt.rtp:prepend(vim.fn.getcwd() .. "/nvim")
local context = require("config.agent_context")
assert(context.relative("/repo/a b", "/repo") == "a b")
assert(context.relative("/repository/a", "/repo") == nil)
assert(context.snippet("a", 2, { "```", "é" }) == "a#L2\n\n````\n```\né\n````")
assert(context.snippet("a", 1, {}) == "a#L1\n\n```\n\n```")
assert(context.location("") == "[unnamed buffer]")
local dir = vim.fn.tempname()
vim.fn.mkdir(dir .. "/nested", "p")
local function git(where, ...)
  assert(vim.system({ "git", "-C", where, ... }):wait().code == 0)
end
git(dir, "init", "-q")
git(dir .. "/nested", "init", "-q")
vim.fn.writefile({ "héllo", "world" }, dir .. "/nested/a b")
assert(context.location(dir .. "/nested/a b") == "a b")
assert(vim.uv.fs_symlink(dir .. "/nested/a b", dir .. "/link"))
assert(context.location(dir .. "/link") == "a b")
assert(context.location(dir .. "/nested/new file") == "new file")
local copied
vim.g.clipboard = {
  name = "test",
  copy = {
    ["+"] = function(lines)
      copied = lines
    end,
    ["*"] = function() end,
  },
  paste = {
    ["+"] = function()
      return {}
    end,
    ["*"] = function()
      return {}
    end,
  },
}
vim.cmd.edit(vim.fn.fnameescape(dir .. "/nested/a b"))
vim.cmd.normal({ "gg0v2l", bang = true })
local cursor = vim.api.nvim_win_get_cursor(0)
context.copy(true)
assert(table.concat(copied, "\n"):find("hél", 1, true))
assert(vim.deep_equal(cursor, vim.api.nvim_win_get_cursor(0)))
vim.cmd.normal({ "\27ggVj", bang = true })
context.copy(true)
assert(table.concat(copied, "\n"):find("héllo\nworld", 1, true))
vim.fn.delete(dir, "rf")
print("agent context tests passed")
vim.cmd("qa!")
