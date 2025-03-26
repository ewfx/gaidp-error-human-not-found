import streamlit as st
import pandas as pd
import json
import pdfplumber
from google import genai
import re

global data_file
global placeholder
global placeholder2
global gemini_api_key
gemini_api_key="your-api-key"

# Function for Determining and Displaying unmatched fields
@st.dialog("Fields Not Found")
def show_unmatched_fields(fields,category):
    st.header("Selected Schedule: "+str(category))
    st.dataframe({"Field Names":fields})

# Function to Check file for extension, and convert to dataframe
def check_excel(file):
    if file is not None:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
            return df
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
            return df
        else:
            st.error("Unsupported file format. Please upload a CSV or XLSX file.")
            return None
    return None

# Function to Decide which schedule to select
def select_rule(df,rules,check_rule=None):
    selected=""
    for rule in rules:
        selected=rule
        unmatched_field=[]
        for field in rules[rule]:
            if str(field) in df.columns.tolist():
                continue
            else:
                selected=""
                if(check_rule==None):
                    break
                else:
                    unmatched_field.append(field)
        if(selected!=""):
            break
    if selected=="":
        if check_rule != None:
            placeholder.write("Schedule selected: "+check_rule+"   :red[(Error: Required fields not found!)]")
            show_unmatched_fields(unmatched_field,check_rule)
            st.session_state["s_rule"]="checkbox"
            return None
        else:
            placeholder.write("No Schedule selected")
            st.session_state["s_rule"]=None
        return None
    else:   
        st.session_state["s_rule"]=selected
        placeholder.write("Schedule selected: "+selected)
        return selected

# Function to check transaction data according to the rules 
def check_transaction(df, rules="rules.json",selected_rule = None):
        if selected_rule == None:
                return None
        all_results=[]
        batch_size = 1
        num_batches = (len(df) - 1) // batch_size + 1  # Adjust for the header row
        batches = [pd.concat([df.iloc[:1], df.iloc[i * batch_size + 1 : (i + 1) * batch_size + 1]]) for i in range(num_batches)]
        client = genai.Client(api_key=gemini_api_key)
        for i, batch in enumerate(batches):
            results=[]
            table_data = pd.DataFrame(batch).to_csv(index=False)
            all_rules= load_json(rules)
            prompt = f"""
            Transaction Data:
            {table_data}
            Rules:
            {all_rules[selected_rule]}
            For every field (Column) in Transaction Data, compare with the corresponding field in Rules.
            Mark any field that does not follow the condition mentioned for that field in the rule as anomaly.
            Output the results only for anomaly found in {batch_size} Transaction Data in the Given Format: (Array of JSON)
            {{
            "Record Index": <index number>,
            "Field Name": <field name which caused the rule-breach>,
            "Value": <value>,
            "Rule": single rule that was broken,
            "Remediation": <solution to remove the anomaly>,
            }}
            """
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            try:
                results=extract_json_from_text(response.text,r_type="array")
                df_res=pd.DataFrame(results)
            except:
                results=response.text+"}]"
                results=list(results)
                results=results[0:-1]
            all_results.extend(results)
        df_res=pd.DataFrame(all_results)
        return df_res

# Function to load rules file
def load_json(rules="rules.json"):
    try:
        with open(rules, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        st.error("Invalid or missing JSON file.")
    return {}

# Fucntion to save rules file
def save_json(data):
    with open("rules.json", "w") as file:
        json.dump(data, file, indent=4)

# Function to extract json from Gemini output
def extract_json_from_text(response_text,r_type="json"):
    if(r_type=="json"):
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                st.error("Failed to parse JSON from AI response.")
        return {}
    else:
        match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                st.error("Failed to parse JSON from AI response.")
        return []

#Convert Rules file to csv.
def create_rule_csv(rules="rules.json"):
    for key in list(rules.keys()):
        df=pd.DataFrame(rules[key])
        df.to_csv("../test/"+key+".csv", index=False)

# Function to create side bar as per rules
def create_options(options):
    global placeholder2
    if options:
        fix_key=1
        with st.sidebar:
            st.sidebar.header("ADD RULES & REGULATIONS")
            if st.sidebar.button("Edit Rules",use_container_width=True):
                st.session_state.page="editor"
                st.rerun()
            placeholder2=st.empty()
            st.divider()
            for category, subcategories in options.items():
                with st.sidebar.expander(category):
                    checkbox=st.checkbox("Use this schedule",key="checkbox_"+category,on_change=deselect_others, args=(f"checkbox_"+category,))
                    if checkbox:
                        placeholder2.write(":red[Selected Schedule:] "+str(category))
                        if data_file != None:
                            select_rule(check_excel(data_file),{category:options[category]},category)
                        else:
                            st.session_state["s_rule"]=None
                    fix_key+=1
                    for subcategory in subcategories:
                        info=st.button(subcategory,type="tertiary",key=fix_key)
                        fix_key+=1
                        if info:
                            show_description(category,subcategory)
    pdf_file = st.sidebar.file_uploader("Upload PDF File", type=["pdf"])
    if pdf_file and "name" not in st.session_state:
        if st.sidebar.button("Upload"):
            st.rerun()
            add_new_rule(pdf_file,options)
        add_new_rule(pdf_file,options)
        create_rule_csv(load_json())
    if "name" in st.session_state:
        del st.session_state.name

# Function to allow selecting one schedule at a time
def deselect_others(selected_key):
    for key in st.session_state.keys():
        if key.startswith("checkbox_") and key != selected_key:
            st.session_state[key] = False

# Fucntion to refine rules using AI
def create_rules(text_content, df):
    client = genai.Client(api_key=gemini_api_key)
    results={}
    batch_size = 10
    num_batches = (len(df) - 1) // batch_size + 1  # Adjust for the header row
    batches = [pd.concat([df.iloc[:1], df.iloc[i * batch_size + 1 : (i + 1) * batch_size + 1]]) for i in range(num_batches)]
    
    for i, batch in enumerate(batches):
        table_data = batch.to_csv(index=False)
        prompt = f"""The Text Content and Table Data contains instructions for report of transaction data.
            Refine the rules without missing any information. Output the result of {batch_size} fields mentioned in Table Data in the following format.
            Output format (JSON): {{
                "field_name without (....)": {{
                    "Mandatory":(True/False)(Default: True)
                    "Condition":(Read the Record for the field and specify the format and other restrictions on the field.)(array of smaller rules)
                }}
            }}
            Text Content:
            {text_content}
            Table Data:
            {table_data}
            After answering forget everything we've talked about so far. This is a completely new conversation, so please don't refer to any previous information.
            """
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        results.update(extract_json_from_text(response.text))
    return results

# Function for new window for pdf upload
@st.dialog("New Rule")
def add_new_rule(pdf_file,options):
    new_name = st.text_input("Name: ")
    page_numbers = st.text_input("Page Number (e.g., 1-3): ")
    pdf_run_button = st.button("Extract Rules")
    if pdf_run_button:
        with st.spinner("Processing... Please wait."):
            page_range = page_numbers.split("-")
            if len(page_range)==1:
                page_range.append(page_range[0])
            pages = list(range(int(page_range[0]) - 1, int(page_range[1])))
            
            text_content = ""
            table_content = []
            
            with pdfplumber.open(pdf_file) as pdf:
                for page_num in pages:
                    page = pdf.pages[page_num]
                    text_content += page.extract_text() or ""
                    tables = page.extract_tables()
                    table_content.extend(tables)
            
            csv_table=[table_content[0][0]]
            for rows in table_content:
                for row in rows:
                    if (csv_table[0][0]!=row[0] and row[1] != "DO NOT USE"):
                        if (row[0]==""):
                            for i in range(len(csv_table[-1])):
                                csv_table[-1][i] = csv_table[-1][i] + row[i]
                        else:
                            csv_table.append(row)
            df = pd.DataFrame(csv_table) if table_content else pd.DataFrame()
            df.to_csv("tables.csv", index=False)
            
            rules = create_rules(text_content, df)
            if new_name:
                options[new_name] = rules
                save_json(options)
                st.success("Rules added successfully!")
                st.session_state.name = new_name
                st.rerun()

# Function for new window to display rules for specific field
@st.dialog("Field Description",width="large")
def show_description(category,subcategory):
    st.header(subcategory)
    options = load_json()
    st.write("Mandatory: "+str(options[category][subcategory]["Mandatory"]))
    st.dataframe({"Conditions":options[category][subcategory]["Condition"]},use_container_width=True)
    # st.write("Extracted Rules: "+str(options[category][subcategory]["Condition"]))

# Function for main screen and excel upload
def main_screen():
    global placeholder
    global data_file

    st.title("Gen-AI Data Profiling")
    st.header("Upload Data File")
    data_file = st.file_uploader("Upload XLSX/CSV", type=["xlsx", "csv"])
    if data_file:
        data_file = data_file
        df=check_excel(data_file)
        placeholder=st.empty()
        if "s_rule" not in st.session_state or st.session_state["s_rule"] == None:
            st.session_state["s_rule"] = select_rule(df,load_json())
            selected_rule=st.session_state["s_rule"]
        else:
            selected_rule=st.session_state["s_rule"]
        run_button = st.button("Run", icon="▶",type='primary')
        if run_button:
            if selected_rule == None or selected_rule == "checkbox":
                selected_rule = None
                placeholder.write(":red[Cannot proceed as appropriate schedule is not selected.]")
                deselect_others("None")
            with st.spinner("Processing... Please wait."):
                results = check_transaction(df,selected_rule=selected_rule)
                if results is not None:
                    st.write("Results:")
                    st.dataframe(results,hide_index=True)
                    st.download_button(
                        label="📥 Download Results",
                        data=results.to_csv(index=False).encode("utf-8"),
                        file_name="Report.csv",
                        mime="text/csv",
                    )
    create_options(load_json())
# Function to allow edit access to auditors
def data_editor_page():
    st.title("Data Editor")
    
    st.sidebar.header("Navigation")
    if st.sidebar.button("Back to Main Page",use_container_width=True):
        st.session_state.page = "main"
        st.rerun()
    
    st.sidebar.header("Rules")
    options = load_json()
    for category in options.keys():
        if st.sidebar.button(category,use_container_width=True):
            st.session_state.selected_category = category

    if "selected_category" in st.session_state:
        st.header(f"Editing: {st.session_state.selected_category}")
        data = options.get(st.session_state.selected_category, {})
        data_arr=[] 
        for key in list(data.keys()):
            for condition in data[key]["Condition"]:
                data_arr.append([key,condition])
        df = pd.DataFrame(data_arr)

        edited_df = st.data_editor({"Field Name":df[0],"Condition":df[1]},
            use_container_width=True, 
            hide_index=True,
            num_rows="dynamic",
        )

        if st.button("Save Changes"):
            updated_data = {}

            for index in range(len(edited_df["Field Name"])):
                field_name = edited_df["Field Name"][index]
                condition = edited_df["Condition"][index]

                if field_name in updated_data:
                    updated_data[field_name]["Condition"].append(condition)
                else:
                    if field_name in list(data.keys()):
                        updated_data[field_name] = {"Mandatory": data[field_name]["Mandatory"], "Condition": [condition]}
                    else:
                        updated_data[field_name] = {"Mandatory": False, "Condition": [condition]}

            # Save updated data back to the JSON structure
            options[st.session_state.selected_category] = updated_data
            save_json(options)
            st.success("Changes saved successfully!")

# Navigation bar
st.markdown("""
<style>

    header {
        background: #d71e28 !important;  
        height: 5rem !important;  
    }
</style>
""", unsafe_allow_html=True)

# Display Main page
if "page" not in st.session_state:
    st.session_state.page = "main"

# Display Data Editor Page
if st.session_state.page == "editor":
    data_editor_page()
else:
    main_screen()