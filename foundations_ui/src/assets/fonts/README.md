# ----- Overview ----- #
We only load a certain subset of possible font file extensions because fonts are extremely hard on the browser in terms of rendering engines.  The extensions that we have chosen follow the recommendations here https://css-tricks.com/snippets/css/using-font-face/ .  It supports IE9+

If you only have a font in a certain extension, there are tools online to convert it to the other types.  There is not one specific tool that is recommended at this time but this one works well http://www.font2web.com/.

## Notes ##
* Font file paths in Sass are relative to deployed CSS file paths, not Sass source paths
* Only load .woff2, .woff, and .ttf font files and be sure to load them in that order

Example declaration 
```
@font-face {
  font-family: 'fontFamily';
  src: url('/public/fonts/fontFamily.woff2') format('woff2'), url('/public/fonts/fontFamily.woff') format('woff'),url('/public/fonts/fontFamily.ttf') format('truetype');
  font-weight: normal;
  font-style: normal
}
```