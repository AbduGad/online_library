#!/usr/bin/python3
"""
Contains class BaseModel
"""
from models.engine.db_storage import DBStorage
from models.book import Books
from models.tags import Tags
from models import storage
import unittest
unittest.TestLoader.sortTestMethodsUsing = None


class TestYourClass(unittest.TestCase):
    def test_00_new_obj(self):
        print("1-------------------")
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
        print("2----------------------------------")
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

        # print(storage.all())
        self.assertEqual(storage.count(Books), 3)

        self.assertEqual(storage.count(Tags), 2)

        self.assertEqual(storage.count(), 5)

        storage.close()
        storage.drop_dataBase()

    def test_02_delete_function(self):
        print("3-------------------------")
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

        learnPython = Books(
            name="learn python", author="blue", path="/")
        learnPython.tags.append(fun_tag)
        learnPython.tags.append(educational_tag)
        learnPython.save()

        learnCpp = newbook1 = Books(
            name="learn cpp in 5 days", author="ahmed", path="/")
        learnCpp.tags.append(educational_tag)
        learnCpp.save()

        learn_dataStructure = newbook1 = Books(
            name="learn data structure", author="ibrahem", path="/")
        learn_dataStructure.tags.append(educational_tag)
        learn_dataStructure.save()

        get_fun_tag = storage.getBy_name(Tags, "fun")
        get_educational_tag = storage.getBy_name(Tags, "educational")

        get_learnPython = storage.get(Books, learnPython.id)
        get_learnCpp = storage.get(Books, learnCpp.id)

        get_data_structure = storage.getBy_name(
            Books, name="learn data structure")

        # with self.assertRaises(ValueError):
        #     storage.all(None)

        with self.assertRaises(TypeError):
            storage.all(str)

        # self.assertEqual(storage.count(), 5
        # for key, value in (storage.all()).items():
        #     print("555555555555555", key, value)

        self.assertEqual(len(storage.all()), 5)


if __name__ == '__main__':
    # TestYourClass().test_new_obj()
    # TestYourClass().test_all_function()
    unittest.main()

    # TestYourClass().xtest_all_function()
    # db = DBStorage(database_name="test_db", check_create_database=True)

    # db.reload()

    # newbook1 = Books(name="test_book1", author="test_auther1", path="/")
    # db.new(newbook1)
    # db.save()

    # newbook2 = Books(name="test_book2", author="test_auther2", path="/")

    # db.new(newbook2)
    # print("66666666", newbook2.id)
    # db.save()

    # newbook3 = Books(name="test_book3", author="test_auther3", path="/")

    # db.new(newbook3)
    # db.save()

    # tag1 = Tags(name="test_tag1")
    # db.new(tag1)
    # db.save()

    # tag2 = Tags(name="test_tag2")
    # db.new(tag2)
    # db.save()

    # db.close()
