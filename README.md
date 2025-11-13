# AI Test Generators
A simple project to leverage the use of AI chatbot APIs for a focused generation of tests.

The scripts are very basic as an introductory approach to using AI APIs. They currently just use a user story defined in the main function to form the prompt.

Example output:

```
> python3 testgenerator_gemini.py                                   
Requirement: The clinician dashboard must allow the user to filter patient records by 'Sleep Apnea Severity' and export the resulting list as a CSV file. The export process must not take longer than 5 seconds for up to 1000 records.

--- Sending request to Gemini LLM...
--- Successfully Generated Test Cases (via Gemini) ---
[
    {
        "id": "TC-F001",
        "type": "Functional",
        "description": "Verify filtering patient records by 'Mild' Sleep Apnea Severity.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Locate the 'Sleep Apnea Severity' filter control.",
            "Select 'Mild' from the filter options."
        ],
        "expected_result": "Only patient records with 'Sleep Apnea Severity' classified as 'Mild' are displayed on the dashboard."
    },
    {
        "id": "TC-F002",
        "type": "Functional",
        "description": "Verify filtering patient records by 'Severe' Sleep Apnea Severity.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Locate the 'Sleep Apnea Severity' filter control.",
            "Select 'Severe' from the filter options."
        ],
        "expected_result": "Only patient records with 'Sleep Apnea Severity' classified as 'Severe' are displayed on the dashboard."
    },
    {
        "id": "TC-F003",
        "type": "Functional",
        "description": "Verify clearing the 'Sleep Apnea Severity' filter.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Apply a 'Sleep Apnea Severity' filter (e.g., 'Moderate').",
            "Clear the applied filter (e.g., select 'All' or 'None' option)."
        ],
        "expected_result": "All patient records, regardless of 'Sleep Apnea Severity', are displayed on the dashboard."
    },
    {
        "id": "TC-F004",
        "type": "Functional",
        "description": "Verify exporting a filtered list of patient records as a CSV file.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Apply a 'Sleep Apnea Severity' filter that yields multiple records (e.g., 'Mild').",
            "Click the 'Export as CSV' button."
        ],
        "expected_result": "A CSV file containing only the filtered patient records is downloaded. The file name should be descriptive (e.g., 'PatientRecords_MildSleepApnea_YYYYMMDD.csv')."
    },
    {
        "id": "TC-F005",
        "type": "Functional",
        "description": "Verify the content and structure of the exported CSV file for filtered data.",
        "steps": [
            "Execute TC-F004 to download a filtered CSV file.",
            "Open the downloaded CSV file using a spreadsheet editor.",
            "Verify that the column headers are correct and consistent.",
            "Verify that only records matching the applied 'Sleep Apnea Severity' filter are present.",
            "Verify the data integrity and accuracy for a sample of records within the CSV."
        ],
        "expected_result": "The CSV file contains accurate headers, only the patient records matching the filter, and correct data for those records."
    },
    {
        "id": "TC-F006",
        "type": "Functional",
        "description": "Verify exporting an unfiltered list of all patient records as a CSV file.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Ensure no 'Sleep Apnea Severity' filter is applied (all available records should be displayed).",
            "Click the 'Export as CSV' button."
        ],
        "expected_result": "A CSV file containing all displayed patient records is downloaded. The file name should be descriptive (e.g., 'PatientRecords_All_YYYYMMDD.csv')."
    },
    {
        "id": "TC-F007",
        "type": "Functional",
        "description": "Verify exporting a filtered list when no patient records match the applied filter.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Apply a 'Sleep Apnea Severity' filter that is known to result in no matching patient records (e.g., a specific value not present in the test data).",
            "Verify that no patient records are displayed on the dashboard.",
            "Click the 'Export as CSV' button."
        ],
        "expected_result": "An empty CSV file (or a CSV with only headers) is downloaded, or a clear message indicating no records to export is displayed, without any errors or crashes."
    },
    {
        "id": "TC-F008",
        "type": "Functional",
        "description": "Verify that exporting a list of 500 records completes within 5 seconds.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Ensure patient records are displayed such that applying a filter or no filter results in exactly 500 records.",
            "Start a stopwatch/timer.",
            "Click the 'Export as CSV' button.",
            "Stop the stopwatch/timer immediately after the CSV file download is complete."
        ],
        "expected_result": "A CSV file containing 500 patient records is downloaded successfully, and the entire export process (from click to file completion) takes no longer than 5 seconds."
    },
    {
        "id": "TC-F009",
        "type": "Functional",
        "description": "Verify that exporting a list of 1000 records completes within 5 seconds.",
        "steps": [
            "Navigate to the Clinician Dashboard.",
            "Ensure patient records are displayed such that applying a filter or no filter results in exactly 1000 records.",
            "Start a stopwatch/timer.",
            "Click the 'Export as CSV' button.",
            "Stop the stopwatch/timer immediately after the CSV file download is complete."
        ],
        "expected_result": "A CSV file containing 1000 patient records is downloaded successfully, and the entire export process (from click to file completion) takes no longer than 5 seconds."
    },
    {
        "id": "TC-N001",
        "type": "Negative",
        "description": "Attempt to export patient records when dashboard data retrieval fails or is unavailable.",
        "steps": [
            "Simulate a scenario where the patient data retrieval API fails, or the dashboard displays an error message indicating no data.",
            "Navigate to the Clinician Dashboard and verify that no patient records are loaded or an error state is visible.",
            "Attempt to click the 'Export as CSV' button."
        ],
        "expected_result": "The 'Export as CSV' button is disabled, or clicking it results in an appropriate error message (e.g., 'No data available to export'). The system should not attempt to export partial, erroneous, or empty data unexpectedly."
    },
    {
        "id": "TC-N002",
        "type": "Negative",
        "description": "Attempt to export patient records during a network interruption.",
        "steps": [
            "Navigate to the Clinician Dashboard and ensure a filtered list of patient records is displayed.",
            "Click the 'Export as CSV' button.",
            "Immediately after clicking the button, simulate a network disconnection (e.g., disable Wi-Fi/Ethernet or block network traffic)."
        ],
        "expected_result": "The application should detect the network issue and display an appropriate error message (e.g., 'Network error during export', 'Download failed'). The system should handle the interruption gracefully without crashing or freezing."
    }
]

Total Test Cases Generated: 11

```