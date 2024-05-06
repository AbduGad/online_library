from datetime import datetime
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Table, Index
from models.tags import Tags
from models.book import Books
from models.base_model import BaseModel, Base


# from .base_model import BaseModel, Base
# from .book import Books
# from .tags import tags


class Books_tags(Base):
    __tablename__ = 'book_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)

    # book_id = Column("books_id", String(60), ForeignKey("books.id"))

    book_name = Column(
        "book_name",
        String(100),
        ForeignKey("books.name"), primary_key=True
    )

    tag_name = Column(String(100), ForeignKey("tags.name"), primary_key=True)
    # tag_id = Column("tags_id", String(60), ForeignKey("tags.id"))


# Books_tags = Table(
#     'book_tags', Base.metadata,
#     Column('books_id', String(60), ForeignKey('books.id')),
#     Column('tags_id', String(60), ForeignKey('tags.id'))
# )
if __name__ == "__main__":
    connect_str = """mysql+mysqldb://root:123@localhost/lib_db3"""

    engine = create_engine(connect_str, echo=True)
    Base.metadata.create_all(engine)

    if not database_exists(engine.url):
        create_database(engine.url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # book = Books(name="3aml el b7ar", auther="ahmed amr", path="/c")
    book = Books()
    book.name = "3aml el b7ar"
    book.author = "ahmed amr"
    book.path = "/c"
    # book.created_at = "2000-05-15 15:42:18.893217"
    # book.updated_at = "2000-05-15 15:42:18.893217"
    # print("out -----------", book.created_at)
    # print("out -----------", book.updated_at)
    tag = session.query(Tags).filter(Tags.name.contains("comedy"))
    print("---------", tag)
    if tag.first() is not None:
        book.tags.append(tag.first())

    else:
        tag = Tags(name="comedy")
        book.tags.append(tag)

    session.add(book, tag)
    session.commit()
    print("-doneee--")
