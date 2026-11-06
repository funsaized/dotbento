local M = {}

function M.relative(path, root)
  root = root:gsub("/+$", "")
  return path:sub(1, #root + 1) == root .. "/" and path:sub(#root + 2) or nil
end

function M.location(name)
  if name == "" then
    return "[unnamed buffer]", "unnamed buffer"
  end
  local absolute = vim.fn.fnamemodify(name, ":p")
  -- Resolve the file itself, so a symlink into another repo belongs to its target.
  local path = vim.uv.fs_realpath(absolute)
  if not path then
    local parent = vim.uv.fs_realpath(vim.fs.dirname(absolute))
    path = parent and (parent .. "/" .. vim.fs.basename(absolute)) or absolute
  end
  if vim.fn.executable("git") == 1 then
    local env = vim.fn.environ()
    for key in pairs(env) do
      if key:match("^GIT_") then
        env[key] = nil
      end
    end
    local result = vim
      .system({ "git", "-C", vim.fs.dirname(path), "rev-parse", "--show-toplevel" }, {
        text = true,
        env = env,
        clear_env = true,
      })
      :wait()
    if result.code == 0 then
      local root = vim.uv.fs_realpath(((result.stdout or ""):gsub("\n$", "")))
      local relative = root and M.relative(path, root)
      if relative then
        return relative, "repository: " .. root
      end
    end
  end
  return path, "absolute path (Git root unavailable)"
end

function M.snippet(path, line, lines)
  local body = table.concat(lines, "\n")
  local longest = 2
  for run in body:gmatch("`+") do
    longest = math.max(longest, #run)
  end
  local fence = string.rep("`", longest + 1)
  return path .. "#L" .. line .. "\n\n" .. fence .. "\n" .. body .. "\n" .. fence
end

function M.copy(visual)
  local path, origin = M.location(vim.api.nvim_buf_get_name(0))
  local line = vim.api.nvim_win_get_cursor(0)[1]
  local text
  if visual then
    local first, last = vim.fn.getpos("v"), vim.fn.getpos(".")
    local lines = vim.fn.getregion(first, last, {
      type = vim.fn.mode(),
      exclusive = vim.o.selection == "exclusive",
    })
    line = math.min(first[2], last[2])
    text = M.snippet(path, line, lines)
  else
    text = path .. "#L" .. line
  end
  vim.fn.setreg("+", text, "v")
  vim.notify(
    "Copied context to +; "
      .. origin
      .. (vim.bo.modified and "; unsaved buffer content, path names disk location" or "")
  )
end

return M
