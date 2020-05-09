# adapted from https://www.bryanklein.com/blog/hugo-python-gsheets-oh-my/

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import os
import json

output_path = Path("content/claims/")

[ os.remove(output_path / f) for f in os.listdir(output_path) if not f.startswith("_") and f.endswith(".md") ]

# Get JSON_DATA from the build environment.
jsondict = json.loads(os.environ['JSON_DATA'])

# Use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(jsondict, scope)
client = gspread.authorize(creds)

# Open the Google Sheet by ID.
claimsheet = client.open_by_key("12DNrTnPvQRDM_w7TYlwFqll7vPZLp-7i4HKO3uXdYts").worksheet("Database")

# Extract all of the records for each row.
records = claimsheet.get_all_records()

# Set location to write new files to.

# Loop through each row...
for row in records:
  if row.get("Approved") == "yes":
    # Open a new file with filename based on the first column
    filename = row.get("Claim").lower().replace(" ", "-") + '.md'
    outputfile = output_path / filename
    new_yaml = open(outputfile, 'w')

    # Empty string that we will fill with YAML formatted text based on data extracted from our CSV.
    yaml_text = ""
    yaml_text += "---\n"
    #_yaml_text += "draft: false\n"
    yaml_text += "title: \"" + row.get("Claim") + "\"\n"
    yaml_text += "draft: false\n"

    # Set the Page title value.
    #yaml_text += "title: \"Left Answers: " + row.get("Claim") + "\".\n"

    # Write our YAML string to the new text file and close it.
    new_yaml.write(yaml_text + "---\n\n")
    new_yaml.write(row.get("Response"))
    new_yaml.write("\n\n")
    new_yaml.close()
