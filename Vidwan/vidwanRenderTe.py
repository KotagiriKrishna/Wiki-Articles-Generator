import ast
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from itertools import zip_longest
from vidwan_genxml import tewiki, writePage

def getVDWResearcherData(row ):
    #name, domain, present_work_state, present_workplace, present_designation, address, DOB
    #Qualification_data
    #experience_data, present_workplace
    #research_interests, Articles, Conferences, Books, Projects
    # Awards_data
    #profmemb_data

    education= sort_education(row['Qualification']) 

    if row['Qualification_Te'] or row['qual_inst_Te'] or row['qual_yrs']:
        Qualification_data = zip_longest(row['Qualification_Te'], row['qual_inst_Te'], row['qual_yrs'], fillvalue="")
    else:
        Qualification_data = zip_longest([''],[''],[''])

    if row['Exp_yrs'] or row['Exp_inst_Te'] or row['Designation_Te']:
        experience_data = zip_longest(row['Exp_yrs'], row['Exp_inst_Te'], row['Designation_Te'], fillvalue="")
    else:
        experience_data = zip_longest([''],[''],[''])

    if row['award_yrs'] or row['award_inst_Te'] or row['Award_Te'] :
        Awards_data = zip_longest(row['award_yrs'], row['award_inst_Te'], row['Award_Te'], fillvalue="0")
    else:
        Awards_data = zip_longest([''],[''],[''])
    
    if row['Professional Bodies'] or row['prof_validity']:
        profmemb_data = zip_longest(row['Professional Bodies_Te'], row['prof_validity_Te'], fillvalue="")
    else:
        profmemb_data = zip_longest([''],[''])

    #print(row['Exp_inst'])

    Scientists_data = {
        'name': str(row['name_Te']),  
        'domain': str(row['domain_Te']),
        "education":education,
        'present_work_state': str(row['work_place_Te']),
        'present_workplace': str(row['present_inst_Te']),
        'present_designation': str(row['present_desig_Te']), 
        'address': str(row['Home_Te']),
        'birth_date': str(row['DOB']),
        'gender': str(row["gender_Te"]),
        'occupation' : str(row['present_desig']),
        'Qualification_data': Qualification_data,
        'experience_data': experience_data,
        'research_interests': row["interest_Te"],
        'Articles': str(row["Articles"]),
        'Conferences': str(row["Conferences"]),
        'Books': str(row["Books"]),
        'Projects': str(row["Projects"]),
        'Awards_data' : Awards_data,
        "profmemb_data" : profmemb_data
    }
    return Scientists_data

def xmlGen(sample_df,template , count, end ):
    fobj = open('C:/Users/krishna/OneDrive/Documents/Scientists/Telugu xml files/Indian_prof_articles'+str(count)+'.xml', 'w',  encoding='utf-8')
    fobj.write(tewiki + '\n')

    # Professor info
    count = 0
    for index, row in sample_df.iterrows():
        title = row[0]

        scient_data = getVDWResearcherData(row)
    
        text = template.render(scient_data)
        if (index == len(sample_df)-1) or index == end:
            writePage(title, text, fobj,1)
        else:
            writePage(title, text, fobj,0)


def remove_non_printable(text):
    if isinstance(text, str):
        return text.replace('\u200C', '').replace('\u200B', '')  
    return text

def str_literal(string_data):
    cleaned_data = string_data.strip("[]")
    list_data = [item.strip(" '") for item in cleaned_data.split("', '")]

    return (list_data)


def converter(obj):
    L=[]
    if obj and obj not in [ [""], "0" , 0, None]:
        for i in ast.literal_eval(obj):
            L.append(i)
        return L

def sort_education(education):
    l =[]
    if education and education not in [ [""], "0" , 0, None]:
        for i in education:
            if (i[0]) =="P":
                return i
            
        for i in education:
            if (i[0]) =="M":
                return i
            
        for i in education:
            if (i[0]) =="P":
                return i 

def Dataset_processing(df_researchinfo):

    df_researchinfo["Exp_yrs"]= [converter(i) for i in df_researchinfo["Exp_yrs"]] 
    df_researchinfo["qual_yrs"]= [converter(i) for i in df_researchinfo["qual_yrs"]]
    df_researchinfo["award_yrs"]= [converter(i) for i in df_researchinfo["award_yrs"]]

    df_researchinfo["Qualification"]= [converter(i) for i in df_researchinfo["Qualification"]]
    df_researchinfo["Qualification_Te"]= [converter(i) for i in df_researchinfo["Qualification_Te"]]
    df_researchinfo["Exp_inst_Te"]= [converter(i) for i in df_researchinfo["Exp_inst_Te"]]
    df_researchinfo["Designation_Te"]= [converter(i) for i in df_researchinfo["Designation_Te"]]
    df_researchinfo["interest_Te"]= [converter(i) for i in df_researchinfo["interest_Te"]]
    df_researchinfo["qual_inst_Te"]= [converter(i) for i in df_researchinfo["qual_inst_Te"]]

    df_researchinfo["award_inst_Te"]= [str_literal(i) for i in df_researchinfo["award_inst_Te"]]  # string literal

    df_researchinfo["Award_Te"]= [converter(i) for i in df_researchinfo["Award_Te"]]
    df_researchinfo["Professional Bodies_Te"]= [converter(i) for i in df_researchinfo["Professional Bodies_Te"]]
    df_researchinfo["prof_validity_Te"]= [converter(i) for i in df_researchinfo["prof_validity_Te"]]
    df_researchinfo = df_researchinfo.fillna("0")

    return df_researchinfo

def main():
    file_loader = FileSystemLoader('')
    env = Environment(loader=file_loader, newline_sequence='\n', keep_trailing_newline=True)
 
    template = env.get_template('Tel_sci_template.j2')

    #Accessing Data from GOOGLE SHEETS
    sheet_url = "https://docs.google.com/spreadsheets/d/1u0lzx5kvdl9uSH1E58cSnWNTpeOPw7mUzBff8dgAPos/export?format=csv"
    df_researchinfo = pd.read_csv(sheet_url , encoding='utf-8')
    df_researchinfo = df_researchinfo.fillna(0)


    #df_researchinfo = pd.read_excel("C:/Users/krishna/OneDrive/Documents/Scientists/Datasets/Vidwan_Dataset.xlsx")

    df_researchinfo = Dataset_processing(df_researchinfo)
    start=0
    step = 1  # no of records in each XML File
    count =1 
    # Using Loop for dividing the data into parts
    for i in range(step, 2 ,step):  #len(df_researchinfo),step):
        xmlGen(df_researchinfo.iloc[start:i,:] , template, count, i-1)
        start = i
        count += 1

    #xmlGen(df_researchinfo.iloc[start:len(df_researchinfo) , :] ,template , count, len(df_researchinfo)-1) 
       

if __name__ == '__main__':
    main()
   