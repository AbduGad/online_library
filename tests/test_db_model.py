#!/usr/bin/python3
"""
Contains class BaseModel
"""
import os
import sys

# from tests.set_test_env import set_testEnv, set_parent_dir
# ? import set_test_env

os.environ['test_db'] = 'true'

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(parent_dir)

from models.engine.db_storage import DBStorage
from models.book import Books
from models.tags import Tags
from models import storage
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class TestYourClass(unittest.TestCase):
    def test_00_new_obj(self):
        newbook = Books(name="test_book_first", author="test_auther", path="/")
        storage.new(newbook)
        storage.save()
        book: Books = storage.getBy_name(Books, name="test_book_first")
        self.assertNotEqual(book, None)
        self.assertEqual(book.name, "test_book_first")
        self.assertEqual(book.author, "test_auther")
        self.assertEqual(book.path, "/")

        #######
        with self.assertRaises(ValueError):
            storage.new(None)

        #####
        with self.assertRaises(TypeError):
            storage.new("wrong type test")

        with self.assertRaises(TypeError):
            storage.new(111)

        storage.close()
        storage.drop_dataBase()

    def test_01_all_function(self):
        storage.reload()

        newbook1 = Books(name="test_book1", author="test_auther1", path="/")
        storage.new(newbook1)
        storage.save()

        self.assertEqual(newbook1.name, "test_book1")
        self.assertEqual(newbook1.author, "test_auther1")

        self.assertEqual(newbook1.path, "/")

        newbook2 = Books(name="test_book2", author="test_auther2", path="/")
        self.assertEqual(newbook2.name, "test_book2")
        self.assertEqual(newbook2.author, "test_auther2")
        self.assertEqual(newbook2.path, "/")

        storage.new(newbook2)
        storage.save()

        newbook3 = Books(
            name="test_book3",
            author="test_auther3",
            path="/",
        )
        self.assertEqual(newbook3.name, "test_book3")
        self.assertEqual(newbook3.author, "test_auther3")
        self.assertEqual(newbook3.path, "/")
        storage.new(newbook3)
        storage.save()

        tag1 = Tags(name="test_tag1")
        storage.new(tag1)
        storage.save()
        self.assertEqual(tag1.name, "test_tag1")

        tag2 = Tags(name="test_tag2")
        storage.new(tag2)
        storage.save()
        self.assertEqual(tag2.name, "test_tag2")

        self.assertEqual(storage.count(Books), 3)

        self.assertEqual(storage.count(Tags), 2)

        self.assertEqual(storage.count(), 5)

        storage.close()
        storage.drop_dataBase()

    def test_02_delete_function(self):
        self.assertEqual(None, None)
        storage.reload()

        newbook1 = Books(name="test_book1", author="test_auther2", path="/")
        newbook1.save()

        newbook2 = Books(name="test_book2", author="test_auther2", path="/")
        newbook2.save()

        newbook3 = Books(name="test_book3", author="test_auther2", path="/")
        newbook3.save()

        tag1 = Tags(name="test_tag1")
        tag1.save()

        tag2 = Tags(name="test_tag2")
        tag2.save()

        book1 = storage.get(Books, "random id ")

        self.assertEqual(book1, None)
        self.assertEqual(newbook1.name, "test_book1")
        self.assertNotEqual(newbook1.name, "test_book")

        self.assertEqual(newbook2.name, "test_book2")
        self.assertEqual(newbook3.name, "test_book3")
        self.assertEqual(tag1.name, "test_tag1")

        book1 = storage.getBy_name(Books, "test_book1")
        book2 = storage.getBy_name(Books, "test_book2")
        book3 = storage.getBy_name(Books, "test_book3")

        self.assertEqual(book1.name, "test_book1")
        self.assertEqual(book2.name, "test_book2")
        self.assertEqual(book3.name, "test_book3")

        tag1 = storage.getBy_name(Tags, "test_tag1")
        tag2 = storage.getBy_name(Tags, "test_tag2")

        storage.delete(book1)
        storage.delete(book2)
        storage.delete(book3)
        book1 = storage.getBy_name(Books, "test_book1")
        book2 = storage.getBy_name(Books, "test_book2")
        book3 = storage.getBy_name(Books, "test_book3")

        self.assertEqual(book1, None)
        self.assertEqual(book2, None)
        self.assertEqual(book3, None)

        storage.delete(tag1)
        storage.delete(tag2)

        tag1 = storage.getBy_name(Tags, "test_tag1")
        tag2 = storage.getBy_name(Tags, "test_tag2")

        self.assertEqual(tag1, None)
        self.assertEqual(tag2, None)
        storage.close()

        storage.drop_dataBase()

    def test_03_edgeCases(self):
        storage.reload()

        educational_tag = Tags(name="educational")
        educational_tag.save()

        fun_tag = Tags(name="fun")
        fun_tag.save()

        learnPython = Books(name="learn python", author="blue", path="/")
        learnPython.tags.append(fun_tag)
        learnPython.tags.append(educational_tag)
        learnPython.save()

        learnCpp = newbook1 = Books(
            name="learn cpp in 5 days", author="ahmed", path="/"
        )
        learnCpp.tags.append(educational_tag)
        learnCpp.save()

        learn_dataStructure = newbook1 = Books(
            name="learn data structure", author="ibrahem", path="/"
        )
        learn_dataStructure.tags.append(educational_tag)
        learn_dataStructure.save()

        get_fun_tag = storage.getBy_name(Tags, "fun")
        get_educational_tag = storage.getBy_name(Tags, "educational")

        get_learnPython = storage.get(Books, learnPython.id)
        get_learnCpp = storage.get(Books, learnCpp.id)

        get_data_structure = storage.getBy_name(
            Books, name="learn data structure")

        with self.assertRaises(TypeError):
            storage.all(str)

        self.assertEqual(len(storage.all(None)), 5)

        from models.book_tags import Books_tags

        self.assertFalse(
            any(isinstance(item, Books_tags) for item in storage.all(None))
        )

        self.assertNotEqual(get_learnPython.name, None)
        self.assertTrue(isinstance(get_learnPython.name, str))

        self.assertEqual(len(get_learnPython.tags), 2)
        self.assertEqual(len(get_data_structure.tags), 1)
        self.assertEqual(len(get_learnCpp.tags), 1)

        #!test tags_book relation
        self.assertIn((get_learnPython.tags)[0].name, ("fun", "educational"))
        self.assertIn((get_learnPython.tags)[1].name, ("fun", "educational"))
        self.assertIn((get_learnCpp.tags)[0].name, ("educational"))
        self.assertIn((get_data_structure.tags)[0].name, ("educational"))
        #! test delete
        storage.delete(get_learnPython)
        get_learnPython = storage.getBy_name(Books, "learn python")
        self.assertEqual(get_learnPython, None)

        storage.delete(get_learnCpp)
        get_learnPython = storage.get(Books, "learn cpp in 5 days")
        self.assertEqual(get_learnPython, None)

        storage.delete(get_data_structure)
        get_data_structure = storage.get(Books, "learn data structure")
        self.assertEqual(get_data_structure, None)

        storage.delete(get_fun_tag)
        get_fun_tag = storage.get(Tags, "fun")
        self.assertEqual(get_fun_tag, None)

        storage.delete(get_educational_tag)
        get_educational_tag = storage.get(Tags, "educational")
        self.assertEqual(get_educational_tag, None)

        self.assertEqual(0, storage.count(None))

        #!################## Edge cases ###############
        with self.assertRaises(TypeError):
            storage.new("")

        # delete function
        with self.assertRaises(ValueError):
            storage.delete(None)

        with self.assertRaises(TypeError):
            storage.delete(str)

        with self.assertRaises(TypeError):
            storage.delete(Books)

        with self.assertRaises(ValueError):
            storage.delete(None)

        # get function
        self.assertEqual(storage.get(None, ""), None)

        self.assertEqual(storage.get(get_learnPython, ""), None)

        self.assertEqual(storage.get(get_learnPython, ""), None)

        with self.assertRaises(TypeError):
            storage.get(str, "")

        with self.assertRaises(TypeError):
            storage.get("None", "")

        # get by name function

        self.assertEqual(storage.getBy_name(None, ""), None)

        with self.assertRaises(TypeError):
            storage.get(str, "")

        with self.assertRaises(TypeError):
            storage.get("None", "")

        # count function edge cases

        with self.assertRaises(TypeError):
            storage.count(123)

        with self.assertRaises(TypeError):
            storage.count("unsupported type")
        ####################################
        storage.close()
        storage.drop_dataBase()


if __name__ == "__main__":
    unittest.main()
