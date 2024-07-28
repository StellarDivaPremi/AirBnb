import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings
import json

warnings.filterwarnings('ignore')
st.set_page_config(page_title="AirBnb- Data Analysis by Premila.M!!!", page_icon=":bar_chart:", layout="wide")
# **********************************************************************************************************
# Define custom CSS to change the background color

custom_css = """
<style>
body {
    background-color: #6F38AD; /* Set your desired background color here */
}
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)

# *********************************************************************************************************************************************

# Streamlit Dashboard UI

file_path1 = r"C:\Users\Admin\projects\Airbnb\\guvi pic.png"
file_path2 = r"C:\Users\Admin\projects\Airbnb\\Airbnb-image.jpg"

# Open the images

image1 = Image.open(file_path1)
image2 = Image.open(file_path2)

# Display the Guvi image and Title
st.title('**GUVI PROJECT**')
st.write("********************************")
st.image(image1, caption='', width=300)

# Display the Airbnb image and Title

st.title(":bar_chart: :blue[airbnb- DATA ANALYSIS]:sunglasses:  ")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.image(image2, caption='', use_column_width=True)

# ***********************************************************************************************************************************************

# Converting json to csv
# Load JSON file
with open(r'C:\Users\Admin\projects\airbnb\data.json') as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('airdata.csv', index=False)

# with st.headbar:
SELECT = option_menu(
    menu_title=None,
    options=["About AirBnb", "Getting more information from Data", "How to Contact Us"],
    icons=["house", "bar-chart", "at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "Pink", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})

#----------------Home----------------------#

if SELECT == "About AirBnb":
 st.header('Airbnb')
 st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
 st.subheader('Skills take away From This Project:')
 st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit and PowerBI')
 st.subheader('Domain:')
 st.subheader('Travel Industry, Property management and Tourism')


if SELECT == "Getting more information from Data":
 fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
 if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
 else:
    os.chdir(r"C:\Users\Admin\Projects\airbnb")
    df = pd.read_csv(r'C:\Users\Admin\Projects\airbnb\data.csv')

 st.sidebar.header("Choose your filter: ")

 # Create for neighbourhood_group
 neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
 if not neighbourhood_group:
     df2 = df.copy()
 else:
     df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

 # Create for neighbourhood
 neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
 if not neighbourhood:
     df3 = df2.copy()
 else:
     df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

 # Filter the data based on neighbourhood_group, neighbourhood

 if not neighbourhood_group and not neighbourhood:
     filtered_df = df
 elif not neighbourhood:
     filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
 elif not neighbourhood_group:
     filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
 elif neighbourhood:
     filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
 elif neighbourhood_group:
     filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
 elif neighbourhood_group and neighbourhood:
     filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
 else:
     filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

 room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

 col1, col2 = st.columns(2)
 with col1:
    st.subheader("room_type_ViewData")
    fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

 with col2:
    st.subheader("neighbourhood_group_ViewData")
    fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
    fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

 cl1, cl2 = st.columns((2))
 with cl1:
    with st.expander("room_type wise price"):
        st.write(room_type_df.style.background_gradient(cmap="Blues"))
        csv = room_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 with cl2:
    with st.expander("neighbourhood_group wise price"):
        neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
        st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
        csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 # Create a scatter plot
 data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
 data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
 st.plotly_chart(data1, use_container_width=True)

 with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
     st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

 # Download orginal DataSet
 csv = df.to_csv(index=False).encode('utf-8')
 st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

 import plotly.figure_factory as ff

 st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
 with st.expander("Summary_Table"):
    df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

 # map function for room_type

# If your DataFrame has columns 'Latitude' and 'Longitude':
 st.subheader("Airbnb Analysis in Map view")
 df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

 st.map(df)

# ----------------------Contact---------------#

if SELECT == "How to Contact Us":
    Name = (f'{"Name :"}  {"Premila Mohanasundaram"}')
    mail = (f'{"Mail :"}  {"Premilamohandharani@gmail.com"}')
    description = "An Architect of Data Engineering !"
    social_media = {
        "Youtube": "https://youtu.be/QKSqy4lXcTA?si=GVyC7RzArboKtlmL",
        "GITHUB": "https://github.com/StellarDivaPremi/AirBnb-Guvi-Project.git",
        "LINKEDIN": "https://www.linkedin.com/in/premila-mohanasundaram-7a703a46/"}

    col1, col2 = st.columns(2)
    col1.image(Image.open(r"C:\Users\Admin\projects\airbnb\aircouples.jpg"), width=550)

    with col2:
        st.header('Airbnb Data Analysis')
        st.subheader(
            "This project aims to analyze Airbnb data using JASON Data, Pyhon , streamlit, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
        st.write("---")
        st.subheader(Name)
        st.subheader(mail)

    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")