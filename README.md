Description: 
Developed a Python script leveraging the Google Analytics Reporting API V4 to automate the generation of customized reports based on specified dimensions and date ranges. The script connects to the Analytics API, retrieves data for multiple views, and writes the results to CSV files for further analysis. Additionally, the script retrieves site URLs associated with each view ID to organize the generated reports into separate folders for enhanced data management.

Key Responsibilities and Achievements:
Initialized an authorized Analytics Reporting API V4 service object to access Google Analytics data securely.
Utilized the get_report() function to query the Analytics API for reports based on specified dimensions and date ranges.
Integrated error handling to gracefully manage exceptions and ensure script robustness during API requests.
Implemented functionality to retrieve site URLs associated with view IDs, enhancing the organization of generated reports.
Employed the os.makedirs() function to dynamically create folders corresponding to each view ID and stored reports within them.
Ensured data integrity by encoding report data in UTF-8 format before writing to CSV files.

Technologies Used:
Python
Google Analytics Reporting API V4
Google API Client Library
OAuth 2.0 for Service Accounts
