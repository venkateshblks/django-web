from django.shortcuts import render,redirect
from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib, base64
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.core.paginator import Paginator

def handle_uploaded_file(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, on_bad_lines='skip')
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            return None, "Unsupported file type."
    except Exception as e:
        return None, str(e)
    # Generate plots
    def generate_plot(data,column, plot_type):
        plt.figure(figsize=(10, 6))
        if plot_type == 'Histogram':
            sns.histplot(data[column], kde=True)
            plt.title('Histograms ')
        elif plot_type == 'scatter':
            if len(data.columns) >= 2:
                sns.scatterplot(x=data.iloc[:, 2], y=data.iloc[:, 1])
                plt.title('Scatter Plot')
            else:
                return None
        elif plot_type == 'Box plot':
            sns.boxplot(y=data[column])
            plt.title('Box Plot')
        elif plot_type == 'Line Plot':
            sns.lineplot(data=data[column])
            plt.title('Line Plot')
        plt.tight_layout()

        # Save the plot to a string buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        return urllib.parse.quote(string)

    plot_uris = {}
    numerical_columns = df.select_dtypes(include=['number']).columns
    for column in numerical_columns:
        plot_uris[column] = {
            'Histogram': generate_plot(df, column, 'Histogram'),
            'Box plot': generate_plot(df, column, 'Box plot'),
            'Line Plot': generate_plot(df, column, 'Line Plot')
        }
    
    return df, plot_uris

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df, plot_uri = handle_uploaded_file(file)

            if df is None:
                return render(request, 'data_analysis_app/upload.html', {'form': form, 'error': plot_uri})

            request.session['data'] = df.to_json()
            request.session['plot_uri'] = plot_uri
            # Perform data analysis

            return redirect('view_data')

    else:
        form = UploadFileForm()
    return render(request, 'data_analysis_app/upload.html', {'form': form})

def view_data(request):
    # file = request.FILES['file']
    # df, plot_uri = handle_uploaded_file(file)
    df_json = request.session.get('data', None)
    if df_json:
        df= pd.read_json(df_json)
        # print(df.type)
        df_html = df.head().to_html()
        soup = BeautifulSoup(df_html, 'html.parser')
        table = soup.find('table')
        table['class'] += ' border-collapse border border-gray-400'
        for th in soup.find_all('th'):
            th['class'] = 'h-full w-full bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-30 border border-gray-100 px-4 py-2 border border-gray-300'
        for td in soup.find_all('td'):
            td['class'] = 'backdrop-blur-3xl bg-white/30 px-4 py-2 border border-gray-300'
        df_html1 = str(soup)

        des = df.describe().to_html()
        soup = BeautifulSoup(des, 'html.parser')
        table = soup.find('table')
        table['class'] += ' border-collapse border border-gray-400'
        for th in soup.find_all('th'):
            th['class'] = 'h-full w-full bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-30 border border-gray-100 px-4 py-2 border border-gray-300'
        for td in soup.find_all('td'):
            td['class'] = 'backdrop-blur-3xl bg-white/30 px-4 py-2 border border-gray-300'
        des = str(soup)

        miss = df.isnull().sum().to_frame('missing').to_html()
        soup = BeautifulSoup(miss, 'html.parser')
        table = soup.find('table')
        table['class'] += ' border-collapse border border-gray-400'
        for th in soup.find_all('th'):
            th['class'] = 'h-full w-full bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-30 border border-gray-100 px-4 py-2 border border-gray-300'
        for td in soup.find_all('td'):
            td['class'] = 'backdrop-blur-3xl bg-white/30 px-4 py-2 border border-gray-300'
        miss = str(soup)
        # ..........................

        # ...............................
        data = {

                'head': df_html1,
                'describe': des,
                'missing_values': miss,
             
            }
        return render(request, 'data_analysis_app/data.html', data,)
    else:
        return redirect('view_data')

# def visualize_data(request):
#     plot_type = request.GET.get('plot_type', None)
#     plot_uri = request.session.get('plot_uri', None)
#     print(plot_type)
#     if plot_type and plot_uris:
#         plot_uri = plot_uris.get(plot_type, None)
#         if plot_uri:
#             return render(request, 'data_analysis_app/visualize.html', { 'plot_uri': plot_uri, 'plot_type': plot_type })
    
#     if plot_uri:
#         return render(request, 'data_analysis_app/visualize.html', {'plot_uri': plot_uri})
#     # else:
#     return redirect('upload_file')
def visualize_data(request):
    d=request.session.get('data', None)
    df= pd.read_json(d)
    col=df.columns[1]
    # print(df.columns[2])
    plot_type = request.GET.get('plot_type', 'Histogram')  
    column = request.GET.get('column',col)  
    plot_uris = request.session.get('plot_uri', None)
    # print(column)
    if plot_uris and column in plot_uris and plot_type in plot_uris[column]:
        plot_uri = plot_uris[column][plot_type]
        # print(plot_uri)
        return render(request, 'data_analysis_app/visualize.html', { 'plot_uri': plot_uri, 'plot_type': plot_type,'column':column,'columns': plot_uris.keys() ,'plot_types': ['Histogram', 'Box plot', 'Line Plot'] })
    
    return redirect('visualize_data')
