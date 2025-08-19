# -*- coding: utf-8 -*-
"""
Project: Automated Synthetic Data Generation
Author: Grzegorz Pieniak

This script demonstrates a complete data pipeline:
1. Synthetic student data generation using Faker (localized to pl_PL).
2. Data analysis with Pandas (summary statistics, groupings).
3. Data export to CSV, Excel, and SQLite database.
4. SQL queries on the exported data.
5. Visualization of distributions and aggregated results.

Educational / demo project for Data Science and Python for Data Analysis.
"""
# !pip install faker pandas openpyxl matplotlib db-sqlite3

import pandas as pd
import random
import sqlite3
from faker import Faker
import matplotlib.pyplot as plt
import pprint

# Initialize Faker and seeds
faker = Faker('pl_PL')
Faker.seed(42)
random.seed(42)

# Parameters
num_students = 300
study_fields = ['Informatyka', 'Automatyka i Robotyka', 'Mechanika i Budowa Maszyn',
                'Mechatronika', 'Elektrotechnika']
subjects = ['Matematyka', 'Fizyka', 'Chemia', 'Mechanika',
            'Elektrotechnika', 'Materiałoznawstwo']
grades_scale = [3.0, 3.5, 4.0, 4.5, 5.0]
skns = [f"SKN{i}" for i in range(1, 11)]  # Student Research Groups (SKN)

# Custom list of voivodeships (Faker doesn't support Polish states natively)
voivodeships = [
    "dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie",
    "małopolskie", "mazowieckie", "opolskie", "podkarpackie", "podlaskie",
    "pomorskie", "śląskie", "świętokrzyskie", "warmińsko-mazurskie",
    "wielkopolskie", "zachodniopomorskie"
]

# Generate synthetic student dataset
data = []
for _ in range(num_students):
    first_name = faker.first_name()
    last_name = faker.last_name()
    student_id = faker.unique.random_int(min=100000, max=999999)
    study_year = random.randint(1, 5)
    study_field = random.choice(study_fields)

    # Random grades per subject
    grades = {subject: random.choice(grades_scale) for subject in subjects}

    # Student Research Group (about 20% without SKN)
    skn = random.choice(skns + [None, None])

    # Library stats
    borrowed_books = random.randint(0, 15)
    not_returned_books = random.randint(0, min(borrowed_books, 5))

    # Contact info & location
    email = faker.email()
    phone = faker.phone_number()
    address = faker.address().replace("\n", ", ")
    city = faker.city()
    zip_code = faker.postcode()
    blood_type = random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
    state = random.choice(voivodeships)

    data.append({
        "Student ID": student_id,
        "First Name": first_name,
        "Last Name": last_name,
        "Email": email,
        "Phone": phone,
        "Address": address,
        "City": city,
        "Voivodeship": state,
        "Postal Code": zip_code,
        "Blood Type": blood_type,
        "Field of Study": study_field,
        "Study Year": study_year,
        "Research Group": skn if skn else "None",
        "Borrowed Books": borrowed_books,
        "Unreturned Books": not_returned_books,
        **grades
    })

# Create DataFrame
df_students = pd.DataFrame(data)
print(df_students.head())

# === Pandas Analysis ===
stats = {}
stats['Average Grades per Subject'] = df_students[subjects].mean().to_dict()
stats['Students per Field'] = df_students['Field of Study'].value_counts().to_dict()
stats['Avg Borrowed Books'] = df_students['Borrowed Books'].mean()
stats['Avg Unreturned Books'] = df_students['Unreturned Books'].mean()
num_in_skn = df_students[df_students['Research Group'] != 'None'].shape[0]
stats['% Students in SKN'] = round(100 * num_in_skn / df_students.shape[0], 2)
stats['Students per Voivodeship'] = df_students['Voivodeship'].value_counts().to_dict()
stats['Blood Type Distribution'] = df_students['Blood Type'].value_counts().to_dict()
stats['Average Grades by Field'] = df_students.groupby("Field of Study")[subjects].mean().to_dict(orient='index')

pprint.pprint(stats)

# === Export Data ===
csv_path = "studenci_fake.csv"
xlsx_path = "studenci_fake.xlsx"
db_path = "studenci_fake.db"

df_students.to_csv(csv_path, index=False)
df_students.to_excel(xlsx_path, index=False)

conn = sqlite3.connect(db_path)
df_students.to_sql("students", conn, if_exists="replace", index=False)

# Example SQL: avg math grade for 3rd-year students
query = """
SELECT AVG(Matematyka) AS avg_math_year3
FROM students
WHERE `Study Year` = 3
"""
avg_math_year3 = pd.read_sql_query(query, conn).iloc[0, 0]
print(f"Average math grade for 3rd-year students: {avg_math_year3:.2f}")
conn.close()

# === Visualizations ===
# Histogram – Math grades
plt.figure(figsize=(10, 6))
plt.hist(df_students["Matematyka"], bins=[3.0, 3.5, 4.0, 4.5, 5.0, 5.5],
         color="lightgreen", edgecolor="black", align='left', rwidth=0.8)
plt.title("Distribution of Math Grades")
plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.xticks([3.0, 3.5, 4.0, 4.5, 5.0])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("distribution_math.png")
plt.close()

# Avg math grade per voivodeship
avg_math_by_voiv = df_students.groupby("Voivodeship")["Matematyka"].mean().sort_values()
plt.figure(figsize=(12, 8))
avg_math_by_voiv.plot(kind='barh', color='cornflowerblue', edgecolor='black')
plt.title("Average Math Grade by Voivodeship")
plt.xlabel("Average Grade")
plt.ylabel("Voivodeship")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("avg_math_voivodeship.png")
plt.close()

# Students per voivodeship
students_by_voiv = df_students["Voivodeship"].value_counts().sort_values()
plt.figure(figsize=(12, 8))
students_by_voiv.plot(kind='barh', color='lightcoral', edgecolor='black')
plt.title("Number of Students by Voivodeship")
plt.xlabel("Number of Students")
plt.ylabel("Voivodeship")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("students_voivodeship.png")
plt.close()

# Avg grades by field of study
avg_grades_by_field = df_students.groupby("Field of Study")[subjects].mean()
plt.figure(figsize=(12, 8))
avg_grades_by_field.plot(kind='bar', edgecolor='black')
plt.title("Average Grades by Field of Study")
plt.xlabel("Field of Study")
plt.ylabel("Average Grade")
plt.ylim(2.5, 5.5)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("avg_grades_field.png")
plt.close()

# Histogram – Physics grades
plt.figure(figsize=(10, 6))
plt.hist(df_students["Fizyka"], bins=[3.0, 3.5, 4.0, 4.5, 5.0, 5.5],
         color="skyblue", edgecolor="black", align='left', rwidth=0.8)
plt.title("Distribution of Physics Grades")
plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.xticks([3.0, 3.5, 4.0, 4.5, 5.0])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("distribution_physics.png")
plt.close()

# Pie chart – SKN membership
skn_counts = df_students['Research Group'].apply(lambda x: 'In SKN' if x != 'None' else 'Outside SKN').value_counts()
plt.figure(figsize=(8, 8))
plt.pie(skn_counts, labels=skn_counts.index, autopct='%1.1f%%',
        colors=['lightgreen', 'lightgray'], startangle=140)
plt.title("Students in Research Groups (SKN)")
plt.tight_layout()
plt.savefig("skn_share.png")
plt.close()
