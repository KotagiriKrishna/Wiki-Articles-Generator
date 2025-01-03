# Wiki-Articles-Generator

The repository "Wiki-Articles-Generator" contains all the information related to Indian Researchers and Scientists from "https://vidwan.inflibnet.ac.in/searchc/search". Using the data from the website, we automatically created the Indian Researchers and Scientists wiki pages in Telugu and Hindi Languages.

DATA files: 
1) Vidwan_Dataset.xlsx : Indian Researchers and Scientists Data 

Data is read from Vidwan_Dataset file to write a template for each Indian Researchers or Scientists. 

Dataset consists columns with English, Telugu and Hindi languages. You can select your chose of languaged columns for creating wiki articles.

JINJA Templates: 
1) Tel_sci_template.j2 : jinja template for the Telugu wiki article 
2) Hi_sci_template.j2 : jinja template for the Hindi wiki article

PYTHON Files:

1) vidwan_genxml.py : It is the common file for generating the wiki artciles it consists of "mediawiki" tags to create wiki pages.

2) vidwanRenderTe.py : It consists of code to create Telugu wiki articles 
        <-----to run use ----> python vidwanRenderTe.py
        After successful execution you can find generated XML files in  ----- Telugu xml files

3) vidwanRenderHi.py : It consists of code to create Hindi wiki articles
        <-----to run use ----> python vidwanRenderHi.py
        After successful execution you can find generated XML files in  ----- Hindi xml files


