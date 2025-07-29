import sys
import os
import random
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.schema import Base, Animal, AnimalTest, TestResult
from utils.db import engine, SessionLocal

# 1. Tabloları temizle ve yeniden oluştur
print("Dropping and recreating all tables...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# 2. Hayvan türleri ve test bilgileri
species_breeds = {
    "Dog": ["Labrador", "Golden Retriever", "German Shepherd"],
    "Cat": ["British Shorthair", "Siamese", "Maine Coon"],
    "Cow": ["Holstein", "Jersey", "Guernsey"]
}

test_types = {
    "blood": [("WBC", "10^9/L"), ("ALT", "U/L"), ("Calcium", "mg/dL"), ("Phosphorus", "mg/dL"), ("RBC", "10^12/L")],
    "urine": [("Protein", "mg/dL"), ("pH", ""), ("Glucose", "mg/dL")],
    "x-ray": [("Bone Density", "g/cm^2"), ("Lesion Size", "cm")],
    "milk": [("Fat", "%"), ("Somatic Cells", "cells/mL"), ("Lactose", "g/dL")]
}

# 3. Hayvanları oluştur
animals = []
start_birth = date(2015, 1, 1)

for i in range(10):
    species = random.choice(list(species_breeds.keys()))
    breed = random.choice(species_breeds[species])
    name = f"{breed[:3]}_{i}"
    birth_date = start_birth + timedelta(days=random.randint(0, 3000))
    animal = Animal(name=name, species=species, breed=breed, birth_date=birth_date)
    animals.append(animal)

session.add_all(animals)
session.commit()

# 4. Testleri ve sonuçları oluştur
start_test_date = date(2024, 1, 1)
test_count = 0
result_count = 0

for animal in animals:
    for i in range(5):
        test_type = random.choice(list(test_types.keys()))
        test_date = start_test_date + timedelta(days=random.randint(0, 200))
        test = AnimalTest(animal_id=animal.id, test_date=test_date, test_type=test_type)
        session.add(test)
        session.flush()

        test_count += 1

        for param, unit in random.sample(test_types[test_type], k=2):
            result = TestResult(
                test_id=test.id,
                parameter=param,
                value=round(random.uniform(0.1, 100.0), 2),
                unit=unit
            )
            session.add(result)
            result_count += 1

session.commit()
session.close()

print(f"✅ Seed data inserted: {len(animals)} animals, {test_count} tests, {result_count} results.")
