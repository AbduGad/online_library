from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Table, Index
from models.base_model import BaseModel, Base



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
