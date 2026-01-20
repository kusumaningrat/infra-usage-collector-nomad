from typing import Dict
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder

class Graph:
    def __init__(self, azure_secrets: Dict[str, str]):
        self.client_id = azure_secrets["clientId"]
        self.tenant_id = azure_secrets["tenantId"]
        self.client_secret = azure_secrets["clientSecret"]

        self.client_credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        self.app_client = GraphServiceClient(self.client_credential)

    async def get_app_only_token(self) -> str:
        scope = "https://graph.microsoft.com/.default"
        token = await self.client_credential.get_token(scope)
        return token.token

    async def close(self):
        await self.client_credential.close()
        