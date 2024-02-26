import logging
import os
from requests.auth import HTTPBasicAuth

main_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

git_repo = "https://gitlab.com/ex-novo-team/sync2jira.git"
source_dir_domains = main_directory + "/domains"
source_dir_implementations = main_directory + "/implementations"
source_dir_config = main_directory + "/config"

pypi_username = "wefine"
pypi_password = "SjKFC3:UHY)es3Q"


#Package dossiers et fichiers
package_dir = "/home/ibtihell/PycharmProjects/sync2jira_package"
destination_dir_domains = package_dir + "/domains"
destination_dir_implementations = package_dir + "/implementations"
destination_dir_config = package_dir + "/config"

setup_file = package_dir + "/setup.py"

log_file = main_directory + "/log/file.log"

table_correspondance_file = main_directory + "/files/correspondance_table.json"

history_file = main_directory + "/files/history.txt"

log_format = '%(asctime)s - %(levelname)s - %(message)s'

database_file = "sqlite:///" + main_directory + "/database/issues_bd.db"

#Username du compte jira
username = "ibtihel@exnovo.io"

#Token du compte jira
api_token = "ATATT3xFfGF0nqgTV-RGN17B9CmizmQD0Mmr5ZY-pU0t8TjTzz0lyX0MNJ0XoNdKNy_t4eq9Is3Gw51Mta-kHF0XrEjKUANWzJM1XpRqS_-wSssC4HOuxeRSHibjeryEzXE6DjypWPBU9uReQt5p1jEJw-7KA3Psfb9I-6R36thuCJ_LKRbM1Ac=FE00A811"

#Jira url de base
jira_url_base = "https://exnovo.atlassian.net/"
#Jira url pour récupérer un ticket
jira_url_ticket = jira_url_base + "rest/api/3/issue/"
#Jira url pour récupérer tout les ticket
jira_url_all = jira_url_base + "rest/api/3/search"

auth = HTTPBasicAuth(username, api_token)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

#La clé - attribut Key du projet
project_key = "10000"
#La clé des tickets - attribut Key du issue
key_issue_type = "10001"

workflow_name = 'Software workflow for project 10000'

last_synchronized_data_in_S2 = '2023-01-11T09:33:44.695+0100'

status_dict_S1_to_S2 = {"status1": "To Do", "status2": "Pret", "status3": "In Progress", "status4": "Done"}
status_dict_S2_to_S1 = {"En attente": "status1", "Pret": "status2", "en cours": "status3", "Qualifications": "status4"}

# statusesS1 = ["status1", "status2", "status3", "status4"]
# jiraStatusName = ["To Do", "Pret", "In Progress", "Done"]
# jiraTransition = ["En attente", "Pret", "en cours", "Qualifications"]


# # Correspondance de S1 à S2
# status_dict_S1_to_S2 = {statusS1: jiraStatusName[i] for i, statusS1 in enumerate(statusesS1)}

# # Correspondance de S2 à S1
# status_dict_S2_to_S1 = {jiraStatus: statusesS1[i] for i, jiraStatus in enumerate(jiraTransition)}

#L'attribut de l'id de S1 dans jira
s1_id_in_jira = "customfield_10034"
s1_class = "S3"

module_to_use = "implementations.implementation_issue_S3"
class_to_use = "IssueImplementationS3"