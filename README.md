akka-html.docset
================

[Dash](http://kapeli.com/dash) docset for the [HTML documentation of akka](http://doc.akka.io/docs/akka/2.2.3/index.html)


## Usage

1. clone this repository

2. add the `akka-html.docset` to your Docsets on Dash

- All pages are categorized as 'Guide'
- The pages `Java Documentation` and `Scala Documentation` have a [TOC](http://kapeli.com/guide/guide#tableOfContents)


### Update with wget

1. Download documentation

    wget -r -k -L  http://doc.akka.io/docs/akka/2.2.3/index.html

2. Move the contents of `doc.akka.io/docs/akka/2.2.3/` to `akka-html.docset/Contents/Resources/Documents/`

3. Run `crawler.py` in `akka-html.docset/Contents/Resources` (requires [BeatufulSoup4](http://www.crummy.com/software/BeautifulSoup/))

4. Restart Dash or re-add docset


### Update with akka-docs

1. Clone https://github.com/akka/akka.git somewhere

2. Checkout the desired version, e.g. `git checkout v.2.2.3`

3. Generate the documentation with `sbt make-site`

4. Move the contents of `<akka-repo>/akka-docs/target/sphinx/html` to `akka-html.docset/Contents/Resources/Documents/`

5. Run `crawler.py` in `akka-html.docset/Contents/Resources` (requires [BeatufulSoup4](http://www.crummy.com/software/BeautifulSoup/))

6. Restart Dash or re-add docset

