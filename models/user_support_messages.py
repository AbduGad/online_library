from sqlalchemy import Column, String, ForeignKey, Integer, Text
from models.base_model import BaseModel, Base

class User_support(Base):
	"""table to store client support messages"""
	__tablename__ = 'user_support'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(127))
	email = Column(String(127))
	message = Column(Text)
