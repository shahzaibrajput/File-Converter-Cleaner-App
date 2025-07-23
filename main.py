import  streamlit as st;
import  pandas as pd;
from io import BytesIO;

st.set_page_config(page_title="📁 File Converter & Cleaner", layout="wide")


# Center aligned title using HTML
st.markdown(
    """
    <h1 style='text-align: center; color: black;'>🎉 Build By Shahzaib Rajput</h1>
    <h2 style='text-align: center; color: #4CAF50;'>📁 File Converter & Cleaner</h2>
    """,
    unsafe_allow_html=True
)


st.write("Upload a CSV or Excel Files to clean data convert formats and download the cleaned file.")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e6f7ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

files = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split('.')[-1]
        df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)

        st.subheader(f"🔎{file.name} - Preview")

        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values in - {file.name}"):
            df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
            st.success("Missing values filled Succesfullly.")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}" , df.columns.tolist(), default=df.columns.tolist())   
        df = df[selected_columns] 
        st.dataframe(df.head())

        if st.checkbox(f'📊 Show Chart - {file.name}') and not df.select_dtypes(include = 'number').empty:
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            
        format_choice = st.radio(
            f"Select Format to Convert - {file.name} to:",
            ["CSV", "Excel"],
            key=file.name
        )

        if st.button(f"Convert & Download {file.name} to {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mine = 'text/csv'
                new_name = file.name.replace(ext, 'csv')
            else:
                df.to_excel(output, index=False)
                mine = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                new_name = file.name.replace(ext, 'xlsx')
            output.seek(0)
            st.download_button("Download Cleaned File", data=output, file_name=new_name, mime=mine)
            st.success(f"Processing {file.name} completed successfully!")
   
