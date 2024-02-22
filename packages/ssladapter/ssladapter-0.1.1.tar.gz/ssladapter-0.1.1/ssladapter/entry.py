from typing import Optional
from requests import Session
from .ssl_adapter import SSLAdapter

def session_ssl_adapter(certfile: str, keyfile: str, password: Optional[str] = None,  cacertfile: Optional[str] = None) -> Session:
    """Creates a new session with the provided SSL adapter

    Args:
        certfile (str): Path to the client certificate file.
        keyfile (str): Path to the client private key file.
        password (Optional[str]): Password for the private key file (optional).
        cacertfile (Optional[str]): Path to the CA certificate file (optional).

    Returns:
        Session: session object
    """
    session = Session()
    session.mount('https://', SSLAdapter(
        certfile=certfile,
        keyfile=keyfile,
        password=password,
        cacertfile=cacertfile))
    return session
