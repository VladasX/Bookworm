import json
import urllib.parse
import urllib.request
from bookworm.models import Book
from django.contrib.staticfiles.templatetags.staticfiles import static

def search_query(search_terms, orderBy="relevance", ):
	"""
	Given a string containing search terms (search_terms), and an optional order by,
	returns a list of results from the Google Books API.
	"""

	#Base URL for Google Books API.
	root_url = 'https://www.googleapis.com/books/v1/volumes?q='

	#Remove special characters.
	query_string = urllib.parse.quote(search_terms)

	#Format the string.
	search_url = '{root_url}{query}&orderBy={orderBy}'.format(
	                root_url=root_url,
	                query='+'.join(search_terms.split(" ")),
	                orderBy=orderBy)

	results = []

	try:
	    #Connect to the Google Books API, and convert the response to a Python dictionary.
		response = urllib.request.urlopen(search_url).read().decode('utf-8')
		json_response = json.loads(response)
		for post in json_response['items']:
			title, linkurl, authors, publisher, publishedDate, description, isbn, averageRating, smallThumbnail, thumbnail, textSnippet, pageCount = (None,)*12

			if "title" in post['volumeInfo']:
				title = post['volumeInfo']['title']
			if "id" in post:
				linkurl = post['id']
			if "authors" in post['volumeInfo']:
				authors = ', '.join(post['volumeInfo']["authors"])
			if "publisher" in post['volumeInfo']:
				publisher = post['volumeInfo']['publisher']
			if "publishedDate" in post['volumeInfo']:
				publishedDate = post['volumeInfo']['publishedDate']
			if "description" in post['volumeInfo']:
				description = post['volumeInfo']['description']
			if "industryIdentifiers" in post['volumeInfo']:
			    isbn = post['volumeInfo']['industryIdentifiers'][0]['identifier']
			if "averageRating" in post['volumeInfo']:
				averageRating = post['volumeInfo']['averageRating']
			if "imageLinks" in post['volumeInfo'] and "smallThumbnail" in post['volumeInfo']['imageLinks']:
					smallThumbnail = post['volumeInfo']['imageLinks']['smallThumbnail']
			if "imageLinks" in post['volumeInfo'] and "thumbnail" in post['volumeInfo']['imageLinks']:
				thumbnail = "http://books.google.com/books/content?id={}&printsec=frontcover&img=1&edge=curl&source=gbs_api".format(linkurl)
			else:
				thumbnail = static('/images/default_book_cover.png')
			if "searchInfo" in post and "textSnippet" in post["searchInfo"]:
				textSnippet = post['searchInfo']['textSnippet']
			if "pageCount" in post['volumeInfo']:
				pageCount = post['volumeInfo']['pageCount']

			results.append({'bookid': linkurl,
							'title': title,
			                'authors': authors,
			                'publisher': publisher,
			                'publishedDate': publishedDate,
			                'description': description,
			                'isbn': isbn,
			                'averageRating': averageRating,
			                'smallThumbnail': smallThumbnail,
			                'thumbnail': thumbnail,
			                'textSnippet': textSnippet,
							'pageCount': pageCount
			                 })

			if not Book.objects.filter(bookid=linkurl).exists():
				Book.objects.create(bookid=linkurl, title=title, authors=authors, publisher=publisher, publishedDate=publishedDate, description=description, isbn=isbn, averageRating=0, thumbnail=thumbnail, textSnippet=textSnippet, pageViews=0, pageCount=pageCount)

		#Return the list of results to the calling function.
		return results

	except:
		print("Error when querying the Google Books API.")