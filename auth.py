# .gitignore should include reference to config.py
import pynetbox
import urllib3
urllib3.disable_warnings()

nb_api_key = "dea33dafd8a1bf0daba55576573c259f2a73d341"
nb_username = "netbox"
nb_password = "NIz8MQMuiO32VwUc3OjK"
nb_url = "https://netbox.int.flexcloud.com.br/"

NETBOX_URL = nb_url
NETBOX_TOKEN = nb_api_key

nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)
nb.http_session.verify = False