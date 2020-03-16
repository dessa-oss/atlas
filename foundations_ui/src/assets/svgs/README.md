# ----- Overview ----- #
SVGs here for reference only and are not used in the site html.  They are instead minified and converted to base64 css representations using the following workflow.  We do this because inline SVGs do not have consistent cross-browser behavior and providing .png fallbacks allows for us to support IE8+.

1. Minify here https://jakearchibald.github.io/svgomg/
2. Base64 encode and convert to .png image fallbacks here http://www.grumpicon.com/