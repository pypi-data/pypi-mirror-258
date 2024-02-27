import os

import config.config


def config_package():
    username = input("Entrez le nom d'utilisateur Jira vous pouvez le moifier plus tard  : ")
    api_token = input("Entrez le token API Jira vous pouvez le modifier plus tard: ")
    jira_url_base = input("Entrez l'URL de base de Jira vous pouvez le modifier plus tard: ")
    project_key = input("Entrez la clé du projet Jira vous pouvez le modifier plus tard : ")
    key_issue_type = input("Entrez la clé du type de ticket Jira vous pouvez le modifier plus tard: ")
    s1_id_in_jira = input("Entrez l'attribut ID du champ à detourner  vous pouvez le modifier plus tard: ")

    module_to_use = input("Entrez le module à utiliser comme S1 : ")
    class_to_use = input("Entrez la classe à utiliser comme S1 : ")

    statusesS1 = [input(f"Entrez le statut {i + 1} pour S1 : ") for i in range(4)]
    jiraStatusName = [input(f"Entrez le nom du statut {i + 1} pour Jira : ") for i in range(4)]
    jiraTransition = [input(f"Entrez la transition {i + 1} pour Jira : ") for i in range(4)]
    status_dict_S1_to_S2 = {statusS1: jiraStatusName[i] for i, statusS1 in enumerate(statusesS1)}
    status_dict_S2_to_S1 = {jiraStatus: statusesS1[i] for i, jiraStatus in enumerate(jiraTransition)}
    print('./config.py')
    with open('config.py', 'w') as fichier_config:
        # Écrire la variable configurée dans le fichier
        fichier_config.write(f"""
import logging
import os
from requests.auth import HTTPBasicAuth \n
main_directory = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(main_directory, "log", "file.log")
table_correspondance_file = os.path.join(main_directory, "files", "correspondance_table.json")
history_file = os.path.join(main_directory, "files", "history.txt")
log_format = '%(asctime)s - %(levelname)s - %(message)s'\n

headers = {{
    "Accept": "application/json",
    "Content-Type": "application/json"
}}

username = "{username}"
api_token = "{api_token}"

auth = HTTPBasicAuth(username, api_token)

jira_url_base = "{jira_url_base}"
project_key = "{project_key}"
key_issue_type = "{key_issue_type}"
s1_id_in_jira = "{s1_id_in_jira}"

statusesS1 = {statusesS1}
jiraStatusName = {jiraStatusName}
jiraTransition = {jiraTransition}

status_dict_S1_to_S2 = {status_dict_S1_to_S2}
status_dict_S2_to_S1 = {status_dict_S2_to_S1}

module_to_use = "{module_to_use}"
class_to_use = "{class_to_use}"


""")
    print("donee")