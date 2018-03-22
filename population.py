import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wad2_project.settings")

import django
django.setup()
from django.contrib.auth.models import Group, Permission
from bookworm.models import Book

def populate():
	book_pages = [
		{"title": "Harry Potter and the Prisoner of Azkaban",
		 "bookid": "y6DeDQAAQBAJ",
		 "authors": "J. K. Rowling",
		 "publisher": "Bloomsbury Publishing",
		 "publishedDate": "2015-08-13",
		 "description": " During his third year at Hogwarts School for Witchcraft and Wizardry, Harry Potter must confront the devious and dangerous wizard responsible for his parents' deaths.",
		 "isbn": "1408865416, 9781408865415",
		 "averageRating": 4.5,
		 "thumbnail": "http://books.google.com/books/content?id=y6DeDQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
		 "textSnippet": "During his third year at Hogwarts School for Witchcraft and Wizardry, Harry Potter must confront the devious and dangerous wizard responsible for his parents&#39; deaths.",
		 "pageCount": 320,
		 "pageViews": 0},

		{"title": "Harry Potter and the Classical World",
		 "bookid": "HgwCgAAQBAJ",
		 "authors": "Richard A. Spencer",
		 "publisher": "McFarland",
		 "publishedDate": "2015-07-06",
		 "description": "J.K. Rowling has drawn deeply from classical sources to inform and color her Harry Potter novels, with allusions ranging from the obvious to the obscure. “Fluffy,” the vicious three-headed dog in Harry Potter and the Sorcerer’s Stone, is clearly a repackaging of Cerberus, the hellhound of Greek and Roman mythology. But the significance of Rowling’s quotation from Aeschylus at the front of Harry Potter and the Deathly Hallows is a matter of speculation. Her use of classical material is often presented with irony and humor. This extensive analysis of the Harry Potter series examines Rowling’s wide range of allusion to classical characters and themes and her varied use of classical languages. Chapters discuss Harry and Narcissus, Dumbledore’s many classical predecessors, Lord Voldemort’s likeness to mythical figures, and magic in Harry Potter and classical antiquity—among many topics.",
		 "isbn": "1476621411, 9781476621418",
		 "averageRating": 2.5,
		 "thumbnail": "http://books.google.com/books/content?id=7HgwCgAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
		 "textSnippet": "This extensive analysis of the Harry Potter series examines Rowling’s wide range of allusion to classical characters and themes and her varied use of classical languages.",
		 "pageCount": 324,
		 "pageViews": 0},

		{"title": "The Irresistible Rise of Harry Potter",
		 "bookid": "Aaug_RnI-xQC",
		 "authors": "Andrew Blake",
		 "publisher": "Verso",
		 "publishedDate": "2002",
		 "description":"As the British state begins to unravel, and as journalists compete to pronounce on the death of Britain, a schoolboy from suburban Surrey who lives for most of the year in a semi-parallel universe becomes the most popular figure in contemporary world literature. Now read on – everyone else does...Harry Potter is English, a home-counties suburban child. An orphan, oppressed and abused by the adults around him, he retreats into a fantasy world where his problems are more elemental; everyday rituals, magic spells and supercharged broomsticks with only the occasional homicidal wizard to worry about. Ironically, as Andrew Blake makes clear, J. K. Rowling rescues her character through the reinvention of that apex of class privilege, the English public school, a literary conceit that problematises Harry Potter's status as a role model and raises important social questions about the state of education in Tony Blair's Britain.Andrew Blake's examination of the Harry Potter phenomenon also raises serious questions about the condition of the publishing industry, the state of bookselling and filmmaking, and the ways in which the Potter consumer campaign has changed our ideas about literature and reading. Blake reflects on how these connections, while drawn up in Britain, act as a template for Harry Potter's international success."
		 "isbn": "1859846661, 9781859846667",
		 "averageRating": 4.5,
		 "thumbnail": "http://books.google.com/books/content?id=Aaug_RnI-xQC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
		 "textSnippet": "Blake's examination of the Potter phenomenon raises serious questions about the condition of the publishing industry, filmmaking, and the ways in which the Potter consumer campaign has changed ideas about literature and reading.",
		 "pageCount": 118,
		 "pageViews": 0},

		 {"title": "Heroism in the Harry Potter Series",
		 "bookid": "1WgGDAAAQBAJ",
		 "authors": "Katrin Berndt, Lena Steveker",
		 "publisher": "Routledge",
		 "publishedDate": "2016-04-22",
		 "description":"Taking up the various conceptions of heroism that are conjured in the Harry Potter series, this collection examines the ways fictional heroism in the twenty-first century challenges the idealized forms of a somewhat simplistic masculinity associated with genres like the epic, romance and classic adventure story. The collection's three sections address broad issues related to genre, Harry Potter's development as the central heroic character and the question of who qualifies as a hero in the Harry Potter series. Among the topics are Harry Potter as both epic and postmodern hero, the series as a modern-day example of psychomachia, the series' indebtedness to the Gothic tradition, Harry's development in the first six film adaptations, Harry Potter and the idea of the English gentleman, Hermione Granger's explicitly female version of heroism, adult role models in Harry Potter, and the complex depictions of heroism exhibited by the series' minor characters. Together, the essays suggest that the Harry Potter novels rely on established generic, moral and popular codes to develop new and genuine ways of expressing what a globalized world has applauded as ethically exemplary models of heroism based on responsibility, courage, humility and kindness."
		 "isbn": "1317122119, 9781317122111",
		 "averageRating": 5,
		 "thumbnail": "http://books.google.com/books/content?id=1WgGDAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
		 "textSnippet": "Taking up the various conceptions of heroism that are conjured in the Harry Potter series, this collection examines the ways fictional heroism in the twenty-first century challenges the idealized forms of a somewhat simplistic masculinity ...",
		 "pageCount": 248,
		 "pageViews": 0},
		]




def add_book(name):
	Book.objects.get_or_create(name=name)
	print("Added book '{}'.".format(name))

if __name__ == "__main__":
	print("Starting Bookworm population script...")
	populate()