from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from typing import Optional


class SSLAdapter(HTTPAdapter):
    """
    Custom SSL adapter for requests.Session to handle SSL certificates and keys.

    This adapter extends the functionality of requests.adapters.HTTPAdapter
    to allow loading SSL certificates, keys, and optionally CA certificates
    for secure connections.

    Args:
        certfile (str): Path to the client certificate file.
        keyfile (str): Path to the client private key file.
        password (Optional[str]): Password for the private key file (optional).
        cacertfile (Optional[str]): Path to the CA certificate file (optional).
    """

    def __init__(self, certfile: str, keyfile: str, password: Optional[str] = None,  cacertfile: Optional[str] = None, *args, **kwargs) -> None:
        self._certfile = certfile
        self._keyfile = keyfile
        self._password = password
        self._cacertfile = cacertfile
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs) -> None:
        self._add_ssl_context(kwargs)
        super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs) -> None:
        self._add_ssl_context(kwargs)
        super().proxy_manager_for(*args, **kwargs)

    def _add_ssl_context(self, kwargs: dict) -> None:
        context = create_urllib3_context()
        context.load_cert_chain(certfile=self._certfile,
                                keyfile=self._keyfile,
                                password=str(self._password) if self._password is not None else None)
        if self._cacertfile:
            context.load_verify_locations(cafile=self._cacertfile)
        kwargs['ssl_context'] = context
