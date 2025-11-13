import os
import json
from google import genai
from google.genai import types

# uses GEMINI_API_KEY environment variable.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

def generate_test_cases(user_requirement: str) -> dict:
    """
    Generates structured test cases (functional and negative) using the Gemini model.

    Args:
        user_requirement: The application requirement or user story text.

    Returns:
        A dictionary containing the generated test cases, or an error message.
    """
    system_instruction = (
        "You are an experienced QA Test Engineer specializing in digital health applications. "
        "Your task is to analyze the provided user requirement and generate a comprehensive "
        "list of functional and negative test cases. The output MUST be a valid JSON list "
        "of objects, and should include at least one negative test case."
    )

    # define the desired JSON structure directly using the response_schema feature.
    
    # Define the structure for a single test case object
    test_case_schema = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "id": types.Schema(type=types.Type.STRING, description="Unique test case ID (e.g., TC-001)."),
            "type": types.Schema(type=types.Type.STRING, description="Type of test case (Functional or Negative)."),
            "description": types.Schema(type=types.Type.STRING, description="A summary of the test purpose."),
            "steps": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="A list of execution steps."),
            "expected_result": types.Schema(type=types.Type.STRING, description="The required outcome of the test.")
        },
        required=["id", "type", "description", "steps", "expected_result"]
    )
    
    # The final output is an array of these test case objects
    output_schema = types.Schema(
        type=types.Type.ARRAY,
        items=test_case_schema
    )

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=output_schema,
    )
    
    user_prompt = f"Generate test cases for the following user requirement: {user_requirement}"

    print("--- Sending request to Gemini LLM...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=[user_prompt],
            config=config,
        )
        
        return json.loads(response.text)

    except Exception as e:
        return {"error": f"An error occurred during API call or JSON parsing: {e}"}

# --- Example Usage ---

if __name__ == "__main__":
    mock_requirement = (
        "The clinician dashboard must allow the user to filter patient records by 'Sleep Apnea Severity' "
        "and export the resulting list as a CSV file. The export process must not take longer than 5 seconds "
        "for up to 1000 records."
    )

    print(f"Requirement: {mock_requirement}\n")

    generated_tests = generate_test_cases(mock_requirement)

    if "error" in generated_tests:
        print(f"Error: {generated_tests['error']}")
    else:
        print("--- Successfully Generated Test Cases (via Gemini) ---")
        # Pretty print the list of test cases
        print(json.dumps(generated_tests, indent=4))
        print(f"\nTotal Test Cases Generated: {len(generated_tests)}")