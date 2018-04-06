
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine



Base = declarative_base()

class  Mail(Base):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key=True)
    mail_time = Column(BigInteger)
    mail_from = Column(String)
    mail_to = Column(String)
    subject = Column(String)
    text_of_body = Column(String)


class Lable(Base):
    __tablename__ = 'lable'
    id = Column(Integer, primary_key=True)
    mail_label= Column(String(250), nullable=False)
    mail_id = Column(Integer, ForeignKey('mail.id'))
    mail = relationship(Mail)


engine = create_engine('sqlite:///mails.db')

Base.metadata.create_all(engine)
