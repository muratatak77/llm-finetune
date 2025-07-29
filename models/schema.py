from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    species = Column(String)
    breed = Column(String)
    birth_date = Column(Date)
    tests = relationship("AnimalTest", back_populates="animal")

class AnimalTest(Base):
    __tablename__ = 'animal_tests'
    id = Column(Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animals.id'))
    test_date = Column(Date)
    test_type = Column(String)
    animal = relationship("Animal", back_populates="tests")
    results = relationship("TestResult", back_populates="test")

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('animal_tests.id'))
    parameter = Column(String)
    value = Column(Float)
    unit = Column(String)
    test = relationship("AnimalTest", back_populates="results")
