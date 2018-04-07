
from sqlalchemy import Column, Integer, Text, ForeignKey, BigInteger, UnicodeText, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()

class  MailTable(Base):
    __tablename__ = 'mailTable'
    id = Column(Integer, primary_key=True)
    mail_id = Column(String(200), unique=True)
    mail_time = Column(BigInteger)
    mail_from = Column(Text)
    mail_to = Column(Text)
    subject = Column(Text)
    text_of_body = Column(UnicodeText)


class Label(Base):
    __tablename__ = 'lable'
    id = Column(Integer, primary_key=True)
    mail_label= Column(Text(250), nullable=False)
    mail_id = Column(String(200), ForeignKey('mailTable.mail_id'))
    mailTable= relationship(MailTable)


engine = create_engine('sqlite:///mails.db')

Base.metadata.create_all(engine)
