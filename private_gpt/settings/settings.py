from typing import Literal

from pydantic import BaseModel, Field

from private_gpt.settings.settings_loader import load_active_settings


class CorsSettings(BaseModel):
    """CORS configuration.

    For more details on the CORS configuration, see:
    # * https://fastapi.tiangolo.com/tutorial/cors/
    # * https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    """

    enabled: bool = Field(
        description="Flag indicating if CORS headers are set or not."
        "If set to True, the CORS headers will be set to allow all origins, methods and headers.",
        default=False,
    )
    allow_credentials: bool = Field(
        description="Indicate that cookies should be supported for cross-origin requests",
        default=False,
    )
    allow_origins: list[str] = Field(
        description="A list of origins that should be permitted to make cross-origin requests.",
        default=[],
    )
    allow_origin_regex: list[str] = Field(
        description="A regex string to match against origins that should be permitted to make cross-origin requests.",
        default=None,
    )
    allow_methods: list[str] = Field(
        description="A list of HTTP methods that should be allowed for cross-origin requests.",
        default=[
            "GET",
        ],
    )
    allow_headers: list[str] = Field(
        description="A list of HTTP request headers that should be supported for cross-origin requests.",
        default=[],
    )


class BasicAuthSettings(BaseModel):
    """Authentication configuration.

    The implementation of the authentication strategy must
    """

    enabled: bool = Field(
        description="Flag indicating if authentication is enabled or not.",
        default=False,
    )
    secret: str = Field(
        description="The secret to be used for authentication. "
        "It can be any non-blank string. For HTTP basic authentication, "
        "this value should be the whole 'Authorization' header that is expected"
    )


class JWTAuthSettings(BaseModel):
    """Authentication configuration for JWT.

    The implementation of the authentication strategy for JWT
    """

    enabled: bool = Field(
        description="Flag indicating if authentication is enabled or not.",
        default=False,
    )
    jwks_url: str = Field(description="The url to download JWKs from for verification")
    ingest_claim: str = Field(
        description="The JWT claim to use to determine if allowed to ingest",
        default="ingest",
    )
    user_id_claim: str = Field(
        description="The JWT claim to use to determine the user_id",
        default="sub",
    )
    audience: str = Field(
        description="The intended audience of the JWT", default="privateGPT"
    )


class ServerSettings(BaseModel):
    env_name: str = Field(
        description="Name of the environment (prod, staging, local...)"
    )
    port: int = Field(description="Port of PrivateGPT FastAPI server, defaults to 8001")
    cors: CorsSettings = Field(
        description="CORS configuration", default=CorsSettings(enabled=False)
    )
    basic_auth: BasicAuthSettings = Field(
        description="Authentication configuration",
        default_factory=lambda: BasicAuthSettings(enabled=False, secret="secret-key"),
    )

    jwt_auth: JWTAuthSettings = Field(
        description="JWT AUTh configuration",
        default_factory=lambda: JWTAuthSettings(
            enabled=False, jwks_url="https://example.com/.well-known/jwks.json"
        ),
    )


class DataSettings(BaseModel):
    local_data_folder: str = Field(
        description="Path to local storage."
        "It will be treated as an absolute path if it starts with /"
    )


class LLMSettings(BaseModel):
    mode: Literal["local", "openai", "sagemaker", "mock"]


class VectorstoreSettings(BaseModel):
    database: Literal["chroma", "qdrant"]
    collection_name: str = Field(
        description="collection name to use in the vector store", default="privateGPT"
    )


class RedisSettings(BaseModel):
    host: str = Field(description="Redis host", default="redis")
    port: int = Field(description="Redis port", default=6379)


class DynamoDBSettings(BaseModel):
    table_name: str = Field(description="Dynamodb Table name", default="dummy_table")


class DocumentstoreSettings(BaseModel):
    database: Literal["disk", "redis", "dynamodb"] = Field(default="disk")
    namespace: str = Field(
        description="Namespace to store the document store in",
        default="private_gpt_documents",
    )
    redis: RedisSettings = Field(
        description="The redis connection settings",
        default_factory=lambda: RedisSettings(host="redis", port=6379),
    )
    dynamodb: DynamoDBSettings = Field(
        description="The dynamodb settings",
        default_factory=lambda: DynamoDBSettings(table_name="dummy_table"),
    )


class IndexstoreSettings(BaseModel):
    database: Literal["disk", "redis", "dynamodb"] = Field(default="disk")
    namespace: str = Field(
        description="Namespace to store the index store in", default="private_gpt_index"
    )
    redis: RedisSettings = Field(
        description="The redis connection settings",
        default_factory=lambda: RedisSettings(host="redis", port=6379),
    )
    dynamodb: DynamoDBSettings = Field(
        description="The dynamodb settings",
        default_factory=lambda: DynamoDBSettings(table_name="dummy_table"),
    )


class LocalSettings(BaseModel):
    llm_hf_repo_id: str
    llm_hf_model_file: str
    embedding_hf_model_name: str


class SagemakerSettings(BaseModel):
    llm_endpoint_name: str
    embedding_endpoint_name: str


class OpenAISettings(BaseModel):
    api_key: str


class UISettings(BaseModel):
    enabled: bool
    path: str


class QdrantSettings(BaseModel):
    location: str | None = Field(
        None,
        description=(
            "If `:memory:` - use in-memory Qdrant instance.\n"
            "If `str` - use it as a `url` parameter.\n"
        ),
    )
    url: str | None = Field(
        None,
        description=(
            "Either host or str of 'Optional[scheme], host, Optional[port], Optional[prefix]'."
        ),
    )
    port: int | None = Field(6333, description="Port of the REST API interface.")
    grpc_port: int | None = Field(6334, description="Port of the gRPC interface.")
    prefer_grpc: bool | None = Field(
        False,
        description="If `true` - use gRPC interface whenever possible in custom methods.",
    )
    https: bool | None = Field(
        None,
        description="If `true` - use HTTPS(SSL) protocol.",
    )
    api_key: str | None = Field(
        None,
        description="API key for authentication in Qdrant Cloud.",
    )
    prefix: str | None = Field(
        None,
        description=(
            "Prefix to add to the REST URL path."
            "Example: `service/v1` will result in "
            "'http://localhost:6333/service/v1/{qdrant-endpoint}' for REST API."
        ),
    )
    timeout: float | None = Field(
        None,
        description="Timeout for REST and gRPC API requests.",
    )
    host: str | None = Field(
        None,
        description="Host name of Qdrant service. If url and host are None, set to 'localhost'.",
    )
    path: str | None = Field(None, description="Persistence path for QdrantLocal.")
    force_disable_check_same_thread: bool | None = Field(
        True,
        description=(
            "For QdrantLocal, force disable check_same_thread. Default: `True`"
            "Only use this if you can guarantee that you can resolve the thread safety outside QdrantClient."
        ),
    )


class Settings(BaseModel):
    server: ServerSettings
    data: DataSettings
    ui: UISettings
    llm: LLMSettings
    local: LocalSettings
    sagemaker: SagemakerSettings
    openai: OpenAISettings
    vectorstore: VectorstoreSettings
    indexstore: IndexstoreSettings
    documentstore: DocumentstoreSettings
    qdrant: QdrantSettings | None = None


"""
This is visible just for DI or testing purposes.

Use dependency injection or `settings()` method instead.
"""
unsafe_settings = load_active_settings()

"""
This is visible just for DI or testing purposes.

Use dependency injection or `settings()` method instead.
"""
unsafe_typed_settings = Settings(**unsafe_settings)


def settings() -> Settings:
    """Get the current loaded settings from the DI container.

    This method exists to keep compatibility with the existing code,
    that require global access to the settings.

    For regular components use dependency injection instead.
    """
    from private_gpt.di import global_injector

    return global_injector.get(Settings)
