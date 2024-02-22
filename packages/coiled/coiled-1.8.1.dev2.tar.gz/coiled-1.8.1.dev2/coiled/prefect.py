try:
    import prefect  # type: ignore # noqa
except ImportError as e:
    raise ImportError("The `coiled.prefect` module requires `prefect` to be installed.") from e

from typing import Optional

import dask.config
from prefect.blocks.core import Block  # type: ignore
from pydantic import Field, SecretStr


class Credentials(Block):
    _block_type_name = "Coiled Credentials"
    _logo_url = "https://blog.coiled.io/_static/logo.svg"
    _documentation_url = "https://docs.coiled.io/user_guide/labs/prefect.html"
    _code_example = """
    ```python
    from coiled.prefect import Credentials

    Credentials.load("BLOCK_NAME").login()
    ```
    """

    token: SecretStr = Field(default=..., description="Coiled API token.")
    account: Optional[str] = Field(default=None, description="Coiled account to use.")

    def login(self):
        dask.config.set({"coiled.token": self.token.get_secret_value(), "coiled.account": self.account})
