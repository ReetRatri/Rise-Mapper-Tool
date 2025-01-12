from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
import os
import zipfile
import json
import re
import difflib
from spellchecker import SpellChecker
from bs4 import BeautifulSoup
import read_SB
import difference
import ast
import shutil
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

global upload_folder_path 
upload_folder_path = ''
global OldFilePath
OldFilePath = 'sdsd'
PageArray = []
global globalIndex
globalIndex = None

def find_matching_elements(arr1, arr2):
    matches = [elem1 for elem1 in arr1 if elem1 in arr2]
    return matches

def find_unmatching_elements(arr1, arr2):
    unmatches = [elem1 for elem1 in arr1 if elem1 not in arr2]
    return unmatches

def string_difference_to_html(old_str, new_str):
    differ = difflib.Differ()
    diff = list(differ.compare(old_str.splitlines(), new_str.splitlines()))
    html_result = []

    for line in diff:
        if line.startswith(' '):
            html_result.append(line[2:])  # Unchanged line
        elif line.startswith('- '):
            html_result.append(f'<del>{line[2:]}</del>')  # Deleted line
        elif line.startswith('+ '):
            html_result.append(f'<ins>{line[2:]}</ins>')  # Added line

    html_code = '\n'.join(html_result)
    return f'<pre>{html_code}</pre>'

def checkSpellingError(file_path):
    spell = SpellChecker()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
    text_without_punctuation = re.sub(r'[:.]', '', text)
    words = text_without_punctuation.split()
    misspelled = spell.unknown(words)
    for word in misspelled:
        print(f"Misspelled word: {word}")

def custom_decode(text):
    invalid_sequences = re.findall(r'\\u[0-9a-fA-F]{4}', text)
    for sequence in invalid_sequences:
        try:
            decoded_char = bytes(sequence.encode('utf-8')).decode('unicode-escape')
            text = text.replace(sequence, decoded_char)
        except UnicodeDecodeError:
            pass  # Handle invalid sequences that can't be decoded
    return text

def delete_all_items(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

UPLOAD_FOLDER = 'upload_folder'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/Zip_extracting', methods=['POST'])
def upload_file2():
    if 'folder' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['folder']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    try:
     
        extract_to_path = './static/story_package'
    
        # Ensure the extraction directory exists and is empty
        if os.path.exists(extract_to_path):
            shutil.rmtree(extract_to_path)
        os.makedirs(extract_to_path, exist_ok=True)
        
        # Extract the zip file to the specified directory
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
        
        # Update the upload_folder_path variable
        global upload_folder_path 
        upload_folder_path = os.path.join(extract_to_path, 'scormcontent', 'index.html')
        
        return redirect(url_for('my_home2'))
        
    except Exception as e:
        return(f"An error occurred: {e}")
       

@app.route('/home')
def my_home2():
 
    if upload_folder_path:
        current_url = request.url
        iframe_src = upload_folder_path
        disable_class = 'disable' if upload_folder_path else ''
    
    return render_template('index.html', iframe_src=iframe_src, disable_class=disable_class)

@app.route('/')
def my_home():
    iframe_src = "d./static/story_package/scormcontent/index.html"    
    print(iframe_src)
    # return render_template('index.html', iframe_src=iframe_src)
    return iframe_src

@app.route('/resetValues')
def reset_Values():
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'])
    global PageArray
    PageArray = []
    delete_all_items(upload_folder)
    return "Done"

@app.route('/loadhtml', methods=['POST'])
def load_html():
    html_file_path = request.form.get('html_file_path')
    try:
        with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            html_content = file.read()
        return html_content
    except Exception as e:
        return str(e)

@app.route('/loadhtmldata', methods=['POST'])
def loadhtmldata():
    html_file_path = request.form.get('html_file_path')
    try:
        dir_path = os.path.dirname(html_file_path)
        with zipfile.ZipFile(html_file_path, 'r') as zip_ref:
            zip_ref.extractall(dir_path)
    except Exception as e:
        return str(e)

@app.route('/contentMismatch', methods=['POST'])
def contentMismatch():
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'])
    delete_all_items(upload_folder)

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    global OldFilePath
    if OldFilePath != file_path:
        global PageArray
        PageArray = []
    OldFilePath = file_path
    final_file_path = os.path.join(os.getcwd(), file_path)

    slideTitle = request.form.get('slideTitle')
    parentDataText = request.form.get('parentDataText')
    storyboardTxtFilePath = read_SB.readSB(slideTitle, final_file_path, parentDataText)
    pageHtml = request.form.get('data')
    pageHtml = pageHtml.replace("", "f")
    htmlpagetext = ''.join(json.loads(pageHtml))
    textincourse = ast.literal_eval(htmlpagetext)

    course_slide_txt = 'Course_slide_' + slideTitle + '.txt'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], course_slide_txt)
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write("Course text" + '\n\n')
        for text in textincourse:
            f.write(text+'\n')

    courseTxt = os.path.join(app.config['UPLOAD_FOLDER'], 'Course_slide_' + str(slideTitle) + '.txt')
    storyboardTxt = os.path.join(app.config['UPLOAD_FOLDER'], 'Storyboard_' + str(slideTitle) + '.txt')
    compareHtmlPath = difference.compareText(courseTxt, storyboardTxt, app.config['UPLOAD_FOLDER'])

    data = {'html_diff': compareHtmlPath}
    return jsonify(data)

@app.route('/comparehtmlsbcourse', methods=['POST'])
def comparehtmlsbcourse():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    final_file_path = os.path.join(os.getcwd(), file_path)
    additional_data = request.form.get('data')
    my_array = json.loads(additional_data)
   
    with open(final_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    paragraphContent = [p.get_text() for p in paragraphs]
    para_list = [item.replace('\n', '') for item in paragraphContent]
    substrings_to_find = ["Alt text:", "Alt  text:"]
    sbALTarray = [item for item in para_list if any(substring in item for substring in substrings_to_find)]
    cleaned_values = [value.replace("  ", " ") for value in sbALTarray]
    split_list = [item.split("Alt text: ")[1] for item in cleaned_values if "Alt text: " in item]

    matching_element = find_matching_elements(my_array, split_list)
    unmatching_element = find_unmatching_elements(my_array, split_list)

    data = {'matchingArray': matching_element, 'unMatchingArray': unmatching_element}
    tables_with_class = soup.find_all('table', class_='MsoTableGrid')
    table_counter = 0
    doc_page_titles = []

    for table in tables_with_class:
        if table_counter < 2:
            table_counter += 1
            continue  # Skip the first two tables

        first_tr = table.find('tr')
        if first_tr:
            first_td = first_tr.find('td')
            if first_td:
                title = first_td.get_text(strip=True)
                doc_page_titles.append(title)

    data['matchingArray'] = matching_element
    data['unMatchingArray'] = unmatching_element
    data['pageTitles'] = doc_page_titles
    return data

@app.route('/updatejson', methods=['POST'])
def updatejson():
    data = request.get_json()
    index = data['index']
    jsonFilePath = os.path.join(app.config['UPLOAD_FOLDER'], 'pageArray.json')
    with open(jsonFilePath, 'w', encoding='utf-8', errors='ignore') as json_file:
        PageArray.insert(index, data)
        json.dump(PageArray, json_file, indent=4)
    return "Updated"

@app.route('/resetIndex', methods=['POST'])
def resetIndex():
    global globalIndex
    globalIndex = None
    return jsonify({'message': 'Index reset'})

@app.route('/addpages', methods=['POST'])
def addPages():
    jsonFilePath = os.path.join(app.config['UPLOAD_FOLDER'], 'pageArray.json')
    data = request.get_json()
    page_data = data['pageData']

    with open(jsonFilePath, 'r', encoding='utf-8', errors='ignore') as json_file:
        PageArray = json.load(json_file)

    global globalIndex
    globalIndex = data.get('index')

    for page in page_data:
        if globalIndex is not None:
            PageArray.insert(globalIndex, page)
            globalIndex += 1
        else:
            PageArray.append(page)

    with open(jsonFilePath, 'w', encoding='utf-8', errors='ignore') as json_file:
        json.dump(PageArray, json_file, indent=4)
    return jsonify({'message': 'Pages added successfully'})

@app.route('/viewjson', methods=['GET'])
def viewjson():
    jsonFilePath = os.path.join(app.config['UPLOAD_FOLDER'], 'pageArray.json')
    if os.path.exists(jsonFilePath):
        with open(jsonFilePath, 'r', encoding='utf-8', errors='ignore') as json_file:
            pageArray = json.load(json_file)
        return jsonify(pageArray)
    else:
        return jsonify({"message": "JSON file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=5000)
