akka-html.docset
================

[Dash](http://kapeli.com/dash) docset for the [HTML documentation of akka](http://doc.akka.io/docs/akka/2.2.3/index.html)


## Usage

1. clone this repository

2. add the `akka-html.docset` to your Docsets on Dash

- All pages are categorized as 'Guide'
- The pages `Java Documentation` and `Scala Documentation` have a [TOC](http://kapeli.com/guide/guide#tableOfContents)


### Update

1. Download documentation

    wget -r -k -L  http://doc.akka.io/docs/akka/2.2.3/index.html

2. Move contentx of `doc.akka.io/docs/akka/2.2.3/` to `akka-html.docset/Contents/Resources/Documents/`

3. Run `crawler.py` in `akka-html.docset/Contents/Resources` (requires [BeatufulSoup4](http://www.crummy.com/software/BeautifulSoup/))

4. Restart Dash or re-add docset

