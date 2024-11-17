import json

def convert_to_django_fixture(input_file_path, output_file_path, model_name):
    """
    Converts a JSON file to a Django fixture format.

    :param input_file_path: Path to the original JSON file
    :param output_file_path: Path to save the converted JSON file
    :param model_name: Name of the Django model in the format 'app_name.model_name'
    """
    with open(input_file_path, 'r') as input_file:
        data = json.load(input_file)

    # Convert each entry in the JSON file
    fixture = [
        {
            "model": model_name,
            "pk": idx + 1,
            "fields": entry
        }
        for idx, entry in enumerate(data)
    ]

    # Save the converted fixture to the output file
    with open(output_file_path, 'w') as output_file:
        json.dump(fixture, output_file, indent=4)
    print(f"Converted JSON saved to {output_file_path}")

# Define the input and output paths
input_file = "dataset.json"  # Path to your original JSON file
output_file = "corrected_dataset.json"  # Path to save the corrected JSON
model_name = "chatbot.faq"  # Replace with your app and model name

# Run the conversion
convert_to_django_fixture(input_file, output_file, model_name)
