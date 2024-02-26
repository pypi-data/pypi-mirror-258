from typing import Optional
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.bridge.pydantic import Field, BaseModel
from llama_index.networks.schema.contributor import (
    ContributorQueryRequest,
)
from pydantic.v1 import BaseSettings, PrivateAttr
from fastapi import FastAPI
import uvicorn


class ContributorServiceSettings(BaseSettings):
    secret: str = Field(..., description="JWT secret.")
    api_version: str = Field(default="v1", description="API version.")
    DEBUG: bool = Field(default=False)

    class Config:
        env_file = ".env", ".env.contributor.service"


class ContributorService(BaseModel):
    query_engine: Optional[BaseQueryEngine]
    config: ContributorServiceSettings
    _fastapi: FastAPI = PrivateAttr()

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, query_engine, config):
        self._fastapi = FastAPI(
            version=config.api_version,
        )

        # routes
        self._fastapi.add_api_route(path="/", endpoint=self.index, methods=["GET"])
        self._fastapi.add_api_route(
            path="/api/query",
            endpoint=self.query,
            methods=["POST"],
        )

        super().__init__(query_engine=query_engine, config=config)

    async def index(self):
        if self.config.DEBUG:
            pass
        return {"message": "Hello World!"}

    async def query(self, request: ContributorQueryRequest):
        result = await self.query_engine.aquery(request.query)
        return {
            "response": result.response,
            "source_nodes": result.source_nodes,
            "metadata": result.metadata,
        }

    @classmethod
    def from_config_file(
        cls, env_file: str, query_engine: BaseQueryEngine
    ) -> "ContributorService":
        config = ContributorServiceSettings(_env_file=env_file)
        return cls(query_engine=query_engine, config=config)

    def __getattr__(self, attr):
        if hasattr(self._fastapi, attr):
            return getattr(self._fastapi, attr)
        else:
            raise AttributeError(f"{attr} not exist")

    @property
    def app(self):
        return self._fastapi


if __name__ == "__main__":
    from llama_index.networks.contributor._example import query_engine

    service = ContributorService.from_config_file(
        ".env.contributor.service", query_engine
    )
    uvicorn.run(service.app, host="0.0.0.0", port=8000, log_level="debug")
