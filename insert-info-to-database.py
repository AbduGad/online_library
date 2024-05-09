#!/usr/bin/python3
from models import storage
from models.book import Books
from models.book_tags import Books_tags
from models.tags import Tags

"""newbook= Books(name='testname', author="testauthor", path="~/")
storage.reload()
storage.new(newbook)
storage.save()

newbook= Books(name='testname2', author="testauthor2", path="~/")
storage.reload()
storage.new(newbook)
storage.save()

newbook= Books(name='testname3', author="testauthor3", path="~/")
storage.reload()
storage.new(newbook)
storage.save()"""

newbook= Books(name='e0ccf91eec6b977a9e00ed384dc285df9c2772e3.pdf', author="Alx", path="../", author_img_path='test_image.jpeg', author_summary='good book u need to read it emacsssssssssss', cover_img_path='test_image.jpeg')
storage.reload()
storage.new(newbook)
storage.save()

newbook= Books(name='emacs sheet.pdf', author="Alx", path="../", author_img_path='test_image.jpeg', author_summary='good book u need to read it sheet for commands on emacs', cover_img_path='test_image.jpeg')
storage.reload()
storage.new(newbook)
storage.save()

newbook= Books(name='malloc.pdf', author="Alx", path="../", author_img_path='test_image.jpeg', author_summary='good book u need to read it example displays on malloc', cover_img_path='test_image.jpeg')
storage.reload()
storage.new(newbook)
storage.save()

newbook= Books(name='Tutorial_Pseudocode.pdf', author="Alx", path="../", author_img_path='test_image.jpeg', author_summary='good book u need to read it. pseudocode tutorial by alx', cover_img_path='test_image.jpeg')
storage.reload()
storage.new(newbook)
storage.save()