-- aether (Omarchy's Neovim colorscheme) paints markdown headings from the
-- palette's red/orange slots, and render-markdown draws a full-width band
-- behind each heading. H1's band comes from DiffText -- the theme's selection
-- color, a saturated orange -- so H1 renders as red text on orange, which is
-- hard to read. Give headings a readable per-level ramp and drop the band.
-- The palette is read in on_highlights, so Omarchy theme hot-reloads still work.
return {
  {
    "bjarneo/aether.nvim",
    opts = function(_, opts)
      opts.on_highlights = function(hl, c)
        for i, fg in ipairs({ c.bright_yellow, c.bright_green, c.blue, c.cyan, c.magenta, c.foreground }) do
          hl["@markup.heading." .. i .. ".markdown"] = { fg = fg, bold = true }
        end
      end
    end,
  },
  {
    "MeanderingProgrammer/render-markdown.nvim",
    opts = { heading = { backgrounds = {} } },
  },
}
