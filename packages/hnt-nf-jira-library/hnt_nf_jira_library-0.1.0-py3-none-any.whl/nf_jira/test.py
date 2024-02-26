from nf_jira import wrapper_nf_jira
from dotenv import load_dotenv
import os

load_dotenv()

jira_api = {
    "USERNAME": os.getenv("USER"),
    "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
    "ISSUE_URL": os.getenv("ISSUE_URL"),
    "DOMAIN_URL": os.getenv("DOMAIN_URL"),
    "FORM_URL": os.getenv("FORM_URL"),
    "CLOUD_ID": os.getenv("CLOUD_ID"),
    "NEXINVOICE_API" : os.getenv("NEXINVOICE_API"),
    "API_KEY_CLIENT" : os.getenv("API_KEY_CLIENT"),
    "API_KEY_AUTH" : os.getenv("API_KEY_AUTH")
}

lib_jira = wrapper_nf_jira(jira_api)

issue_data = lib_jira.get_nf_issue_context('GHN-6')

print(issue_data)