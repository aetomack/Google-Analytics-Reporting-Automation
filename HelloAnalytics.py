from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import sys
import csv
import re
import os
#sys.stdout = open('out.txt', 'w')

# Current issue: No output. 

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly'] # OAuth 2.0 scope. This isn't an issue.
KEY_FILE_LOCATION = 'key.json'
VIEW_ID = [# viewIds
          ]
DIM_NAME = [ #dimensions
            ]
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
  return analytics.reports().batchGet(
    body={
      'reportRequests': [
      {
        'viewId': viewId,
        'dateRanges': [{'startDate': '2014-01-01', 'endDate': 'today'}],
        'dimensions': [{"name": dimension}]
      }]
    }
  ).execute()

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
                        print_response_csv(response, csvwriter)
                    print(f"Report written to {filepath}")
                else:
                    print(f"No response received for viewId: {viewId} and dimension: {dim}")

def print_response_csv(response, csvwriter):
    """Writes the Analytics Reporting API V4 response to a CSV file.

    Args:
        response: An Analytics Reporting API V4 response.
        csvwriter: A CSV writer object.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        # Write headers
        headers = dimensionHeaders + [header.get('name') for header in metricHeaders]
        csvwriter.writerow(headers)

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            # Combine dimensions and metrics values
            row_data = dimensions + [value['values'][0] for value in dateRangeValues]

            # Ensure all values are properly encoded as UTF-8
            row_data = [value.encode('utf-8') if isinstance(value, str) else value for value in row_data]

            csvwriter.writerow(row_data)

if __name__ == '__main__':
    main()