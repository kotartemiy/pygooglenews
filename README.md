# pygooglenews
If Google News had a Python library


Created by Artem from [newscatcherapi.com](https://newscatcherapi.com/) but you do not need anything from us or from anyone else to get the software going, it just works out of the box.

My [blog post about how I did it](https://codarium.substack.com/p/reverse-engineering-google-news-rss)

## Demo

![](pygooglenews-demo.gif)

You might also like to check our [Google News API](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/google-news?endpoint=apiendpoint_5e0fa919-2494-4b20-a212-d186b7e8c3d8) or [Financial Google News API](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/stock-google-news?endpoint=apiendpoint_c70050d2-34ac-4eac-a1b2-09aefb19d1a5)

### Table of Contents
- [About](#about)
- [Examples of Use Cases](#usecase)
- [Working with Google News in Production](#production)
- [Motivation](#motivation)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Documentation](#documentation)
- [Advanced Query Search Examples](#examples)
- [About me](#aboutme)

<a name="about"/>

## **About**

A python wrapper of the Google News RSS feed.

Top stories, topic related news feeds, geolocation news feed, and an extensive full text search feed.

This work is more of a collection of all things I could find out about how Google News functions.

### **How is it different from other Pythonic Google News libraries?**

1. URL-escaping user input helper for the search function
2. Extensive support for the search function that makes it simple to use:
    - exact match
    - in title match, in url match, etc
    - search by date range (`from_` & `to_`), latest published (`when`)
3. Parsing of the sub articles. Almost always, all feeds except the search one contain a subset of similar news for each article in a feed. This package takes care of extracting those sub articles. This feature might be highly useful to ML task when you need to collect a data of similar article headlines

<a name="usecase"/>

## Examples of Use Cases

1. Integrating a news feed to your platform/application/website
2. Collecting data by topic to train your own ML model
3. Search for latest mentions for your new product
4. Media monitoring of people/organizations — PR


<a name="production"/>

## Working with Google News in Production

Before we start, if you want to integrate Google News data to your production then I would advise you to use one of the 3 methods described below. Why? Because you do not want your servers IP address to be locked by Google. Every time you call any function there is an HTTPS request to Google's servers. **Don't get me wrong, this Python package still works out of the box.**

1. NewsCatcher's [Google News API](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/google-news?endpoint=apiendpoint_5e0fa919-2494-4b20-a212-d186b7e8c3d8) — all code is written for you, clean & structured JSON output. Low price. You can test it yourself with no credit card. Plus, [financial version of API](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/stock-google-news?endpoint=apiendpoint_c70050d2-34ac-4eac-a1b2-09aefb19d1a5) is also available.
2. [ScrapingBee API](https://www.scrapingbee.com?fpr=artem26) which handles proxy rotation for you. Each function in this package has `scraping_bee` parameter where you paste your API key. You can also try it for free, no credit card required. See [example](#scrapingbeeexample)
3. Your own proxy — already have a pool of proxies? Each function in this package has `proxies` parameter (python dictionary) where you just paste your own proxies. 

<a name="motivaion"/>

## **Motivation**

I love working with the news data. I love it so much that I created [my own company that crawls for hundreds of thousands of news articles, and allow you to search it via a news API](https://newscatcherapi.com/). But this time, I want to share with the community a Python package that makes it simple to get the news data from the best search engine ever created - [Google](https://news.google.com/).

Most likely, you know already that Google has its own [news service](https://news.google.com/). It is different from the usual Google search that we use on a daily basis (sorry [DuckDuckGo](https://duckduckgo.com/), maybe next time).

**This package uses the RSS feed of the Google News. The [top stories page](https://news.google.com/rss), for example.**

RSS is an XML page that is already well structured. I heavily rely on Feedparser package to parse the RSS feed.

Google News used to have an API but it was deprecated many years ago. (Unofficial) information 
about RSS syntax is decentralized over the web. There is no official documentation. So, I tried my best
to collect all this informaion in one place. 


<a name="installation"/>

## **Installation**

```shell script
$ pip install pygooglenews

```

<a name="quickstart"/>

## **Quickstart**

```python
from pygooglenews import GoogleNews

gn = GoogleNews()

```

### **Top Stories**

```python
top = gn.top_news()
```

### **Stories by Topic**

```python
business = gn.topic_headlines('business')

```

### **Geolocation Specific Stories**

```python
headquaters = gn.geo_headlines('San Fran')

```

### **Stories by a Query Search**

```python
# search for the best matching articles that mention MSFT and 
# do not mention AAPL (over the past 6 month
search = gn.search('MSFT -APPL', when = '6m')

```

---
<a name="documentation"/>

## **Documentation - Functions & Classes**

### **GoogleNews Class**

```python
from pygooglenews import GoogleNews
# default GoogleNews instance
gn = GoogleNews(lang = 'en', country = 'US')

```

To get the access to all the functions, you first have to initiate the `GoogleNews` class.

It has 2 required variables: `lang` and `country`

You can try any combination of those 2, however, it does not exist for all. Only the combinations that are supported by GoogleNews will work. Check the official Google News page to check what is covered:

On the bottom left side of the Google News page you may find a `Language & region` section where you can find all of the supported combinations.


For example, for `country=UA` (Ukraine), there are 2 languages supported:

- `lang=uk` Ukrainian
- `lang=ru` Russian

---

### **Top Stories**

```python
top = gn.top_news(proxies=None, scraping_bee = None)

```

`top_news()` returns the top stories for the selected country and language that are defined in `GoogleNews` class. The returned object contains `feed` (FeedParserDict) and `entries` list of articles found with all data parsed.

---

### **Stories by Topic**

```python
business = gn.topic_headlines('BUSINESS', proxies=None, scraping_bee = None)

```

The returned object contains `feed` (FeedParserDict) and `entries` list of articles found with all data parsed.

Accepted topics are:

- `WORLD`
- `NATION`
- `BUSINESS`
- `TECHNOLOGY`
- `ENTERTAINMENT`
- `SCIENCE`
- `SPORTS`
- `HEALTH`

However, you can find some other topics that are also supported by Google News.

For example, if you search for `corona` in the search tab of `en` + `US` you will find `COVID-19` as a topic.

The URL looks like this: `https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE?hl=en-US&gl=US&ceid=US%3Aen`

We have to copy the text after `topics/` and before `?`, then you can use it as an input for the `top_news()` function.

```python
from pygooglenews import GoogleNews

gn = GoogleNews()
covid = gn.topic_headlines('CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE')

```

**However, be aware that this topic will be unique for each language/country combination.**

---

### **Stories by Geolocation**

```python
gn = GoogleNews('uk', 'UA')
kyiv = gn.geo_headlines('kyiv', proxies=None, scraping_bee = None)
# or 
kyiv = gn.geo_headlines('kiev', proxies=None, scraping_bee = None)
# or
kyiv = gn.geo_headlines('киев', proxies=None, scraping_bee = None)
# or
kyiv = gn.geo_headlines('Київ', proxies=None, scraping_bee = None)

```

The returned object contains `feed` (FeedParserDict) and `entries` list of articles found with all data parsed.

All of the above variations will return the same feed of the latest news about Kyiv, Ukraine:

```python
geo['feed'].title

# 'Київ - Останні - Google Новини'

```

It is language agnostic, however, it does not guarantee that the feed for any specific place will exist. For example, if you want to find the feed on `LA` or `Los Angeles` you can do it with `GoogleNews('en', 'US')`.

The main (`en`, `US`) Google News client will most likely find the feed about the most places.

---

### **Stories by a Query**

```python
gn.search(query: str, helper = True, when = None, from_ = None, to_ = None, proxies=None, scraping_bee=None)

```

The returned object contains `feed` (FeedParserDict) and `entries` list of articles found with all data parsed.

Google News search itself is a complex function that has inherited some features from the standard Google Search.

[The official reference on what could be inserted](https://developers.google.com/custom-search/docs/xml_results)

The biggest obstacle that you might have is to write the URL-escaping input. To ease this process, `helper = True` is turned on by default.

`helper` uses `urllib.parse.quote_plus` to automatically convert the input.

For example:

- `'New York metro opening'` --> `'New+York+metro+opening'`
- `'AAPL -MSFT'` --> `'AAPL+-MSFT'`
- `'"Tokyo Olimpics date changes"'` --> `'%22Tokyo+Olimpics+date+changes%22'`

You can turn it off and write your own query in case you need it by `helper = False`

`when` parameter (`str`) sets the time range for the published datetime. I could not find any documentation regarding this option, but here is what I deducted:

- `h` for hours.(For me, worked for up to `101h`). `when=12h` will search for only the articles matching the `search` criteri and published for the last 12 hours
- `d` for days
- `m` for month (For me, worked for up to `48m`)

I did not set any hard limit here. You may try put here anything. Probably, it will work. However, I would like to warn you that wrong inputs will not lead to an error. Instead, the `when` parameter will be ignored by the Google.

`from_` and `to_` accept the following format of date: `%Y-%m-%d` For example, `2020-07-01` 

---

**[Google's Special Query Terms](https://developers.google.com/custom-search/docs/xml_results#special-query-terms) Cheat Sheet**

Many Google's Special Query Terms have been tested one by one. Most of the core ones have been inherited by Google News service. At first, I wanted to integrate all of those as the `search()` function parameters. But, I realised that it might be a bit confusing and difficult to make them all work correctly.

Instead, **I decided to write some kind of a cheat sheet that should give you a decent understanding of what you could do**.

* Boolean OR Search [ OR ]

```python
from pygooglenews import GoogleNews

gn = GoogleNews()

s = gn.search('boeing OR airbus')

print(s['feed'].title)
# "boeing OR airbus" - Google News

```

* Exclude Query Term [-]

"The exclude (`-`) query term restricts results for a particular search request to documents that do not contain a particular word or phrase. To use the exclude query term, you would preface the word or phrase to be excluded from the matching documents with "-" (a minus sign)."

* Include Query Term [+]

"The include (`+`) query term specifies that a word or phrase must occur in all documents included in the search results. To use the include query term, you would preface the word or phrase that must be included in all search results with "+" (a plus sign).

The URL-escaped version of **`+`** (a plus sign) is `%2B`."


* Phrase Search

"The phrase search (`"`) query term allows you to search for complete phrases by enclosing the phrases in quotation marks or by connecting them with hyphens.

The URL-escaped version of **`"`** (a quotation mark) is **`%22`**.

Phrase searches are particularly useful if you are searching for famous quotes or proper names."

* allintext

"The **`allintext:`** query term requires each document in the search results to contain all of the words in the search query in the body of the document. The query should be formatted as **`allintext:`** followed by the words in your search query.

If your search query includes the **`allintext:`** query term, Google will only check the body text of documents for the words in your search query, ignoring links in those documents, document titles and document URLs."

* intitle

"The `intitle:` query term restricts search results to documents that contain a particular word in the document title. The search query should be formatted as `intitle:WORD` with no space between the intitle: query term and the following word."

* allintitle

"The **`allintitle:`** query term restricts search results to documents that contain all of the query words in the document title. To use the **`allintitle:`** query term, include "allintitle:" at the start of your search query.

Note: Putting **`allintitle:`** at the beginning of a search query is equivalent to putting [intitle:](https://developers.google.com/custom-search/docs/xml_results#TitleSearchqt) in front of each word in the search query."

* inurl

"The `inurl:` query term restricts search results to documents that contain a particular word in the document URL. The search query should be formatted as `inurl:WORD` with no space between the inurl: query term and the following word"

* allinurl

The `allinurl:` query term restricts search results to documents that contain all of the query words in the document URL. To use the `allinurl:` query term, include allinurl: at the start of your search query.


### List of operators that do not work (for me, at least):

1. Most (probably all) of the `as_*` terms do not work for Google News
2. `allinlinks:`
3. `related:`


**Tip**. If you want to build a near real-time feed for a specific topic, use `when='1h'`. If Google captured fewer than 100 articles over the past hour, you should be able to retrieve all of them.

Check the [Useful Links](notion://www.notion.so/Google-News-API-Documentation-b95117b9ecd94076bb1d8cf7c2957d78#useful-links) section if you want to dig into how Google Search works.

Especially, [Special Query Terms](https://developers.google.com/custom-search/docs/xml_results#special-query-terms) section of Google XML reference.

Plus, I will provide some more examples under the [Full-Text Search Examples](notion://www.notion.so/Google-News-API-Documentation-b95117b9ecd94076bb1d8cf7c2957d78#examples) section

---

### **Output Body**

All 4 functions return the `dictionary` that has 2 sub-objects:

- `feed` - contains the information on the feed metadata
- `entries` - contains the parsed articles

Both are inherited from the [Feedparser](https://github.com/kurtmckee/feedparser). The only change is that each dictionary under `entries` also contains `sub_articles` which are the similar articles found in the description. Usually, it is non-empty for `top_news()` and `topic_headlines()` feeds.

**Tip** To check what is the found feed's name just check the `title` under the `feed` dictionary

---
<a name="scrapingbeeexample"/>

## How to use pygooglenews with [ScrapingBee](https://www.scrapingbee.com?fpr=artem26)

Every function has `scrapingbee` parameter. It accepts your [ScrapingBee](https://www.scrapingbee.com?fpr=artem26) API key that will be used to get the response from Google's servers. 

You can take a look at what exactly is happening in the source code: check for `__scaping_bee_request()` function under GoogleNews class

Pay attention to the concurrency of each plan at [ScrapingBee](https://www.scrapingbee.com?fpr=artem26)
 
How to use example:

```python
gn = GoogleNews()

# it's a fake API key, do not try to use it
gn.top_news(scraping_bee = 'I5SYNPRFZI41WHVQWWUT0GNXFMO104343E7CXFIISR01E2V8ETSMXMJFK1XNKM7FDEEPUPRM0FYAHFF5')
```

---

## How to use pygooglenews with proxies

So, if you have your own HTTP/HTTPS proxy(s) that you want to use to make requests to Google, that's how you do it:

```python
gn = GoogleNews()

gn.top_news(proxies = {'https':'34.91.135.38:80'})
```

---
<a name="examples"/>

## **Advanced Querying Search Examples**

### **Example 1. Search for articles that mention `boeing` and do not mention `airbus`**

```python
from pygooglenews import GoogleNews

gn = GoogleNews()

s = gn.search('boeing -airbus')

print(s['feed'].title)
# "boeing -airbus" - Google News

```

### **Example 2. Search for articles that mention `boeing` in title**

```python
from pygooglenews import GoogleNews

gn = GoogleNews()

s = gn.search('intitle:boeing')

print(s['feed'].title)
# "intitle:boeing" - Google News

```

### **Example 3. Search for articles that mention `boeing` in title and got published over the past hour**

```python
from pygooglenews import GoogleNews

gn = GoogleNews()

s = gn.search('intitle:boeing', when = '1h')

print(s['feed'].title)
# "intitle:boeing when:1h" - Google News

```

### **Example 4. Search for articles that mention `boeing` or `airbus`**

```python
from pygooglenews import GoogleNews

gn = GoogleNews()

s = gn.search('boeing OR airbus', when = '1h')

print(s['feed'].title)
# "boeing AND airbus when:1h" - Google News

```

---
<a name="useful-links"/>

## **Useful Links**

[Stack Overflow thread from which it all began](https://stackoverflow.com/questions/51537063/url-format-for-google-news-rss-feed)

[Google XML reference for the search query](https://developers.google.com/custom-search/docs/xml_results)

[Google News Search parameters (The Missing Manual)](http://web.archive.org/web/20150204025359/http://blog.slashpoundbang.com/post/12975232033/google-news-search-parameters-the-missing-manual)

---
<a name="built"/>

## **Built With**

[Feedparser](https://github.com/kurtmckee/feedparser)

[Beutifulsoup4](https://pypi.org/project/beautifulsoup4/)

---
<a name="aboutme"/>

## **About me**

My name is Artem. I ❤️ working with news data. I am a co-founder of [NewsCatcherAPI](https://newscatcherapi.com/) - **Ultra-fast API to find news articles by any topic, country, language, website, or keyword**

If you are interested in hiring me, please, contact me by email - **bugara.artem@gmail.com** or **artem@newscatcherapi.com**

Follow me on 🖋 [Twitter](https://twitter.com/bugaralife) - I write about data engineering, python, entrepreneurship, and memes.

Want to read about how it all was done? Subscribe to [CODARIUM](https://codarium.substack.com/)

thx to Kizy
