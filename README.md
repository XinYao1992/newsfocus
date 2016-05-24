# newsfocus

For Corpus:

1. We are using newswire api of NEW YORK TIME.
2. Our newswire corpus has 11 categories: art, business, opinion, sport, world, travel, style, food, health
	magazine, and science. Each news object has attributes such as : title, published date, content of news
	page etc.
3. The technologies for building corpus: 
	1). We used "requests" to open the news pages, which is the NON-GMO HTTP library for Python. It can
		be used to open the url for each news and get the news html page text containing all the
		html information such as html tages and all the text all the page.
	2). We secondly used "BeautifulSoup". It is a Python library for pulling data out of HTML and XML files.
		For example, if we need a certain data from "<p>" with class of "story-body-text", we just 
		write "p_contents = soup.find_all("p",{'class':"story-body-text"})", which will read all the data
		in <p class="story-body-text"> tage and store the data into variable "p_contents".
	3). Some of news pages only have images or videos. We are trying to extract the page title or page 
		descriptions as much as we can.
4. Different category contains different number of news. The total size of newswire we collected are ...MB.


For indices and search queries:
	In our mapping schema, we defined "my_analyzer" which has snowball analyzer, loowercase, stopwords. For news' properties,
We analyzed "section", "title", "abstract", "content", "byline", "source", "published_date". We also treated "published_date" as 
"date" type with the format "yyyy-MM-dd". 
	We used helpers.bulk to load documents, and stores our big json file into a shelve.
	We applied two queries. One is called "Normal search", which only allows users to search by keywords from all the data we
have. The other one is called "advanced search", which specifies the data category and date range so that our system can return
the best matched results for users.


For user interface:
	We set up a nice Django framework into our project, which improves our user experience. In our UI, you 
can see our team's information, and search the news from the input box, or, you can simply click on the type image which directly
shows all the related news in that field. We show 30 results in one page, and we have "next button" function to get more information.
To reduce the processing time, we also implement Ajax and Javascript functions. 


