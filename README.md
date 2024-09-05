# Port Path Finder

**Port Path Finder** is a simple and efficient tool designed to help users find the geographical coordinates (latitude and longitude) of ports or locations from a list of names provided in CSV or Excel files. It uses geocoding to map location names to coordinates, making it useful for anyone working with port data or any place-based datasets.

## Features

- **Upload File:** Upload your CSV or Excel file containing port or location names.
- **Geocoding:** The app processes each port name to retrieve the corresponding latitude and longitude.
- **Download Output:** After processing, download the file with updated location coordinates in Excel format.
- **Flexible Use:** Originally designed for port names, the app can handle any location data as long as the column is named "Port Name."
- **Error Handling:** A delay is added between requests to minimize geocoding errors.
- **User-Friendly:** Progress tracking and clear status updates are provided during the geocoding process.

## Instructions

1. **Upload File:** Upload a CSV or Excel file that contains a column named "Port Name."
2. **Geocoding Process:** The app will process the port names and display a progress bar during the geocoding process.
3. **Download Results:** Once complete, download the processed file with the latitude and longitude of each port.
4. **Customizable Delay:** A delay of 1 second between each request has been added to avoid errors related to rate limits.

## How It Works

The app uses the **geopy** library to geocode port names by interacting with the OpenStreetMap Nominatim service. For each location, it retrieves the geographical coordinates and appends them to the original dataset, which you can download after processing.
