from sqlalchemy import Column, Integer, Text

from db import Base


class ReRequest(Base):
    __tablename__ = 're_request'
    task_id = Column(Integer, primary_key=True)
    task_str = Column(Text)
    json_data_str = Column(Text)
