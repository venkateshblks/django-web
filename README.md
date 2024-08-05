# Data Analysis Django Web Application

This Django web application allows users to upload CSV or Excel files, perform data analysis using pandas, matplotlib and seaborn and display the results and visualizations on the web interface.

## Features

- **File Upload**: Upload CSV or Excel files.
- **Data Processing**: Display the first few rows, summary statistics, and missing values of the uploaded data.
- **Data Visualization**: Generate and display various plots (Histograms, box plots,Line plots etc.) for the numerical columns in the data.
- **User Interface**: A clean and user-friendly interface with a dropdown to select columns and plot types.


## Screenshots

> ### Upload Page
![Screenshot (40)](https://github.com/user-attachments/assets/345e20aa-e2db-4727-8184-281e5be23c7e)


> ### Data Overview Page
![Screenshot (41)](https://github.com/user-attachments/assets/12daaf71-da3a-4d63-9325-8464cf6898b9)
<br>

![Screenshot (42)](https://github.com/user-attachments/assets/4b474a33-abe9-48c1-832a-234ea80ccf21)


> ### Visualization Page
![Screenshot (43)](https://github.com/user-attachments/assets/e6b1fcb3-5250-431f-9e0d-b5c51e0b5970)
<br>
![Screenshot (45)](https://github.com/user-attachments/assets/f1e6b04b-8791-4270-b562-6b414f45e722)



## Requirements

- Python 
- Django 
- pandas
- matplotlib
- seaborn
- openpyxl
> The required packages are listed in requirements.txt and can be installed with pip install -r requirements.txt.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/venkateshblks/django-web
```
### 2. Create and Activate Virtual Environment
``` bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
cd data_analysis_django_app
```
### 4. Apply Migrations
```bash
python manage.py migrate
```
### 5. Run the Development Server
```bash
python manage.py runserver
```
### 6. Open in Browser
Open your browser and go to http://localhost:8000/ to access the application.


## Usage
### Uploading a File
- Go to the homepage and click on "Upload CSV or Excel File".
- Choose the file you want to upload and click "Upload".
### Viewing Data
- After uploading the file, you will be redirected to the data overview page.
- This page displays the first few rows of the data, summary statistics, and missing values.
### Visualizing Data
- Click on the "View Visualizations" button to go to the visualization page.
- Use the dropdowns to select the column and plot type you want to visualize.
- Click "Generate Plot" to view the visualization.
### Uploading a New File
- You can upload a new file at any time by clicking the "Upload New File" button on the data overview or visualization pages.

## Contributing
**Feel free to submit issues or pull requests.**

