import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import io
import base64

# Custom CSS to beautify the app with a dark theme
st.markdown(
    """
    <style>
    .main {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        color: #f5f5f5; /* White text for better readability */
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1, h2, h3, h4, h5, h6, p, li {
        color: #f5f5f5; /* Ensures all text elements are readable */
    }
    .stFileUploader label {
        color: #f5f5f5; /* Ensure labels are readable */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main function
def main():
    st.title("🚢 Port Path Finder")
    
    st.markdown("### Instructions")
    st.markdown(
        """
        1. Upload your CSV or Excel file containing port names.
        2. The app will geocode each port name to find its latitude and longitude.
        3. You can download the file with the coordinates once the process is complete.
        4. This app was initially created to find the coordinates of ports but it's not just limited to that. As long as the name of the column containing the locations is "Port Name", it will be able to find out the coordinates of those places.
        5. Additionally, I added a delay of 1 second between each request to minimize getting errors.
        """
    )
    
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        
        if file_type == 'csv':
            port_df = pd.read_csv(uploaded_file)
        elif file_type == 'xlsx':
            port_df = pd.read_excel(uploaded_file)
        
        # Display the data
        st.write("### Uploaded Data:")
        st.dataframe(port_df)
        
        # Check if required column exists
        if 'Port Name' in port_df.columns:
            st.write("Processing, please wait...")
            
            # Add columns for latitude and longitude
            port_df['Latitude'] = None
            port_df['Longitude'] = None
            
            # Initialize the geocoder
            geolocator = Nominatim(user_agent="port_geocoder")
            
            total_ports = len(port_df)
            progress_bar = st.progress(0)
            
            for index, row in port_df.iterrows():
                port_name = row['Port Name']
                lat, lon = get_coordinates(port_name)
                port_df.at[index, 'Latitude'] = lat
                port_df.at[index, 'Longitude'] = lon
                
                # Update progress bar
                progress_bar.progress((index + 1) / total_ports)
                
                time.sleep(1)
            
            st.success("Geocoding complete!")
            
            # Provide download link
            st.write("### Download the file with coordinates:")
            download_file(port_df)
        else:
            st.error("The uploaded file must contain a column named 'Port Name'.")
    else:
        st.info("Please upload a file to start.")

# Initialize the geocoder
geolocator = Nominatim(user_agent="port_geocoder")

# Function to geocode ports
def get_coordinates(port_name, retries=3):
    try:
        for attempt in range(retries):
            try:
                location = geolocator.geocode(port_name)
                if location:
                    return location.latitude, location.longitude
                else:
                    return None, None
            except GeocoderTimedOut:
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    raise
    except GeocoderServiceError:
        return None, None

# Function to provide a download link for the DataFrame
def download_file(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="ports_with_coordinates.xlsx">Download Excel File</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
