import os
import json
from openai import OpenAI

# uses OPENAI_API_KEY as an environment variable.
try:
    client = OpenAI()
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    print("Please ensure the OPENAI_API_KEY environment variable is set.")
    exit()

def generate_test_cases(user_requirement: str) -> dict:
    """
    Generates structured test cases (functional and negative) using a Generative AI model.

    Args:
        user_requirement: The application requirement or user story text.

    Returns:
        A dictionary containing the generated test cases, or an error message.
    """
  
    system_prompt = (
        "You are an experienced QA Test Engineer specializing in digital health applications. "
        "Your task is to analyze the provided user requirement and generate a comprehensive "
        "list of functional and negative test cases. The output MUST be a valid JSON list "
        "of objects, and should include at least one negative test case."
    )

    # Using a detailed JSON instruction ensures the model returns a reliable structure.
    json_format_instruction = (
        "Output the result as a single JSON list of objects. Each test case object "
        "must have the following keys: 'id', 'type' (e.g., 'Functional' or 'Negative'), "
        "'description', 'steps' (a list of strings), and 'expected_result'."
    )
    
    full_prompt = f"User Requirement: '{user_requirement}'\n\n{json_format_instruction}"

    print("--- Sending request to LLM...")
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", 
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ]
        )
        
        # Extract and parse the JSON string from the response
        json_output = completion.choices[0].message.content
        return json.loads(json_output)

    except Exception as e:
        return {"error": f"An error occurred during API call or JSON parsing: {e}"}

# --- Example Usage ---

if __name__ == "__main__":
    # Mock User Story (relevant to ResMed's context: clinician access to patient data)
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
        print("--- Successfully Generated Test Cases ---")
        # Pretty print the list of test cases
        print(json.dumps(generated_tests, indent=4))
        print(f"\nTotal Test Cases Generated: {len(generated_tests)}")