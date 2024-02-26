from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sei_seeker_models.base import Base


class TransactionModel(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    address = Column(String)
    price = Column(Integer)
    token_id = Column(Integer)
    seller = Column(String)
    buyer = Column(String)

    collection_id = Column(Integer, ForeignKey('collection.id'))
    collection = relationship("CollectionModel", back_populates="transactions")
