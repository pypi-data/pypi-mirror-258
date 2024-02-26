from typing import Optional
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.callbacks.base import CallbackManager
from llama_index.core.schema import QueryBundle
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.prompts.mixin import PromptMixinType
from llama_index.networks.schema.contributor import ContributorQueryResponse
from pydantic.v1 import BaseSettings, Field
import requests
import asyncio
import aiohttp


class ContributorClientSettings(BaseSettings):
    """Settings for contributor."""

    api_key: str = Field(..., env="API_KEY")
    api_url: str = Field(..., env="API_URL")

    class Config:
        env_file = ".env", ".env.contributor.client"


class ContributorClient(BaseQueryEngine):
    """A remote QueryEngine exposed through a REST API."""

    def __init__(
        self,
        callback_manager: Optional[CallbackManager],
        config: ContributorClientSettings,
    ) -> None:
        self.config = config
        super().__init__(callback_manager)

    @classmethod
    def from_config_file(
        cls, env_file: str, callback_manager: Optional[CallbackManager] = None
    ) -> "ContributorClient":
        """Convenience constructor from a custom env file."""

        config = ContributorClientSettings(_env_file=env_file)
        return cls(callback_manager=callback_manager, config=config)

    def _query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        """Make a post request to submit a query to QueryEngine."""
        # headers = {"Authorization": f"Bearer {self.config.api_key}"}
        headers = {}
        data = {"query": query_bundle.query_str}
        result = requests.post(
            self.config.api_url + "/api/query", json=data, headers=headers
        )
        try:
            contributor_response = ContributorQueryResponse.parse_obj(result.json())
        except Exception as e:
            raise ValueError("Failed to parse response") from e
        return contributor_response.to_response()

    async def _aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        """Make a post request to submit a query to QueryEngine."""
        # headers = {"Authorization": f"Bearer {self.config.api_key}"}
        headers = {}
        data = {"query": query_bundle.query_str}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.config.api_url + "/api/query", json=data, headers=headers
            ) as resp:
                json_result = await resp.json()
            try:
                contributor_response = ContributorQueryResponse.parse_obj(json_result)
            except Exception as e:
                raise ValueError("Failed to parse response") from e
        return contributor_response.to_response()

    def _get_prompt_modules(self) -> PromptMixinType:
        """Get prompt sub-modules."""
        return {}


if __name__ == "__main__":
    client = ContributorClient.from_config_file(env_file=".env.contributor.client")
    res = asyncio.run(client.aquery("Who is paul"))
    print(res)
