import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ModelWrapper:
    _provider_registry = {}

    def __init__(self, provider: str, **kwargs):
        """
        Initialize the model wrapper dynamically
        """
        self.provider = provider.lower()
        self.kwargs = kwargs
        self.model = self._initialize_model()

    @classmethod
    def register_provider(cls, provider_name: str, model_class):
        """
        Register a provider with its associated model class.
        """
        cls._provider_registry[provider_name.lower()] = model_class

    def _initialize_model(self):
        if self.provider not in self._provider_registry:
            raise ValueError(
                f"Unsupported provider: {self.provider}. "
                f"Available providers: {list(self._provider_registry.keys())}"
            )

        model_class = self._provider_registry[self.provider]
        return model_class(**self.kwargs)

    @staticmethod
    def load_config_from_env(provider: str) -> dict:
        """
        Dynamically load the configuration for the specified provider from environment variables.

        Args:
            provider (str): The name of the provider (e.g., 'azure', 'openai').

        Returns:
            dict: Configuration dictionary.
        """

        def to_int(value, default=None):
            """Convert a value to int or return default if conversion fails."""
            try:
                return int(value)
            except (TypeError, ValueError):
                return default

        def to_float(value, default=None):
            """Convert a value to float or return default if conversion fails."""
            try:
                return float(value)
            except (TypeError, ValueError):
                return default

        common_keys = [
            "MODEL_NAME",
            "TEMPERATURE",
            "MAX_TOKENS",
            "TIMEOUT",
            "MAX_RETRIES",
        ]
        azure_keys = [
            "AZURE_DEPLOYMENT",
            "AZURE_API_KEY",
            "AZURE_API_BASE",
            "AZURE_API_VERSION",
        ]
        openai_keys = ["OPENAI_API_KEY", "OPENAI_API_BASE"]

        provider_keys = {
            "azure": azure_keys,
            "openai": openai_keys,
        }

        config = {}

        # Common keys
        config["model"] = os.getenv("MODEL_NAME", "gpt-4")
        config["temperature"] = to_float(os.getenv("TEMPERATURE"), 0.5)
        config["max_tokens"] = to_int(os.getenv("MAX_TOKENS"))
        config["timeout"] = to_int(os.getenv("TIMEOUT"))
        config["max_retries"] = to_int(os.getenv("MAX_RETRIES"), 3)

        # Provider-specific keys
        if provider in provider_keys:
            config.update(
                {
                    key.lower(): os.getenv(key)
                    for key in provider_keys[provider]
                    if os.getenv(key) is not None
                }
            )

        return config

    @classmethod
    def initialize_from_env(cls) -> "ModelWrapper":
        """
        Initialize a ModelWrapper instance dynamically based on environment variables.
        """
        provider = os.getenv("LLM_PROVIDER", "azure").lower().strip()

        config = cls.load_config_from_env(provider)
        logging.info(f"Initializing LLM with provider: {provider} and config: {config}")
        return cls(provider=provider, **config)

    def __call__(self, *args, **kwargs):
        """
        Proxy call to the underlying model.
        """
        return self.model(*args, **kwargs)
