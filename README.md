# Automated-Synthetic-Data-Generation-and-Analysis-with-Python
This project demonstrates the full pipeline of data analysis: - Synthetic student dataset generation with Faker (pl_PL localization). - Data enrichment with custom fields (blood type, study fields, research groups, etc.). - Statistical analysis with Pandas. - Export to CSV, Excel, and SQLite. - SQL querying and visualization with Matplotlib.

# 🧪 Automated Synthetic Data Generation

## 👤 Author
**Grzegorz Pieniak**

## 🎯 Project Overview
This project demonstrates a complete **data analysis pipeline** in Python:

1. **Data Generation**  
   - Synthetic student dataset created with [Faker](https://faker.readthedocs.io/) (`pl_PL` localization).  
   - Custom fields: blood type, research groups, study year, borrowed books, etc.  

2. **Data Analysis with Pandas**  
   - Summary statistics (grades, books, memberships).  
   - Grouped averages (by field of study, by voivodeship).  
   - Pretty-printed dictionary of results.  

3. **Data Export**  
   - Exported in **CSV**, **Excel**, and **SQLite** formats.  

4. **SQL Operations**  
   - Example: average math grade for 3rd-year students via SQL query.  

5. **Data Visualization**  
   - Histograms (math, physics grades).  
   - Bar plots (by field, by voivodeship).  
   - Pie chart (research group membership).  

## 📂 Outputs
- `studenci_fake.csv`  
- `studenci_fake.xlsx`  
- `studenci_fake.db`  
- Plots saved as PNG files  

## 🛠️ Technologies
- **Python 3**  
- **pandas** – data manipulation  
- **faker** – synthetic data generation  
- **sqlite3** – SQL database  
- **matplotlib** – visualization  

Example Visualization
The script produces plots such as:
Distribution of Math Grades
Average Math Grade by Voivodeship
Average Grades by Field of Study
Students in Research Groups (pie chart)

## 🚀 Usage
```bash
pip install faker pandas matplotlib openpyxl
python grzegorz_pieniak_automatyzacja_generowania_danych.py
