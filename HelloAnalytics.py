from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import sys
import csv
import re
import os


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly'] 
KEY_FILE_LOCATION = 'key.json'
VIEW_ID = ['Your view IDs here'] # separate multiple with commas
DIM_NAME = ['ga:yourdimensionhere'] # separate multiple with commas
def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES) 

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics



"""Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
"""
def get_report(analytics, dimension, viewId):
    page_token = None
    all_rows = []

    while True:
        # Create request body with page token if available
        request_body = {
            'reportRequests': [
                {
                    'viewId': viewId,
                    'dateRanges': [{'startDate': '2014-01-01', 'endDate': 'today'}],
                    'dimensions': [{"name": "ga:date"}, {"name": dimension}],
                    'pageToken': page_token
                }
            ]
        }

        # Execute the request
        response = analytics.reports().batchGet(body=request_body).execute()

        # Extract rows from response and append to all_rows
        for report in response.get('reports', []):
            rows = report.get('data', {}).get('rows', [])
            all_rows.extend(rows)

        # Check if there are more pages to fetch
        next_page_token = response.get('reports', [])[0].get('nextPageToken', None)
        if next_page_token:
            page_token = next_page_token
        else:
            break  # No more pages to fetch

    return all_rows

def main():
    analytics = initialize_analyticsreporting()

    for viewId in VIEW_ID:
        view_folder = f"view_{viewId}"
        os.makedirs(view_folder, exist_ok=True)  
        for dim in DIM_NAME:
            # Replace or remove special characters
            filename = re.sub(r'[^\w\s-]', '', dim)
            filepath = os.path.join(view_folder, f"{filename}.csv")
            try:
                response = get_report(analytics, dim, viewId)
            except Exception as e:
                print(f"An error occurred while getting the report for viewId: {viewId} and dimension: {dim}. Exception: ",e)
            else:
                if response:
                    with open(filepath, "w", newline='', encoding='utf-8') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        headers= ["date", dim, "visits"]
                        csvwriter.writerow(headers)
                        print_response_csv(response, csvwriter)
                    print(f"Report written to {filepath}")
                else:
                    print(f"No response received for viewId: {viewId} and dimension: {dim}")

def print_response_csv(all_rows, csvwriter):
    """Writes the Analytics Reporting API V4 response to a CSV file.

    Args:
        all_rows: A list containing all rows retrieved from Google Analytics.
        csvwriter: A CSV writer object.
    """
    # Write headers
    header_written = False
    for row in all_rows:
        if not header_written:
            columnHeader = row.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            headers = dimensionHeaders + [header.get('name') for header in metricHeaders]
            
            # Modify headers to replace special characters and format them properly
            headers = [re.sub(r'[^\w\s-]', '', header).lower() for header in headers if header]
            
            if headers:  # Check if there are any non-empty headers
                csvwriter.writerow(headers)
                header_written = True

        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        # Combine dimensions and metrics values
        row_data = dimensions + [value['values'][0] for value in dateRangeValues]

        # Ensure all values are properly encoded as UTF-8
        row_data = [value.encode('utf-8') if isinstance(value, str) else value for value in row_data]

        csvwriter.writerow(row_data)

        

if __name__ == '__main__':
    main()