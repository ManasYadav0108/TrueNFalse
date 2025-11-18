from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
def get_keyvault_secret(conn_dict):
    vault_url = conn_dict["vault_url"]
    secret_name = conn_dict["secret_name"]

    client = SecretClient(vault_url, DefaultAzureCredential())
    secret = client.get_secret(secret_name)

    return secret.value