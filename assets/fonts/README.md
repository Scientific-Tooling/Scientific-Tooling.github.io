# Site fonts

Manrope provides interface/body text; Source Serif 4 provides display headings.
These unmodified variable WOFF2 files include Latin and Latin Extended subsets
served by Google Fonts on October 27, 2026. Each family's SIL Open Font License
is included alongside the files. Browser fallbacks cover other character sets.

- Manrope: <https://github.com/googlefonts/manrope>
- Source Serif 4: <https://github.com/adobe-fonts/source-serif>
- Distribution: <https://fonts.google.com/>

`theme.css` declares the fonts using root-relative URLs so project pages on this
domain can share them. Pages preload only the two Latin subsets; extended
subsets load on demand. No visitor request to an external font service is needed.
