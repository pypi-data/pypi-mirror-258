from requests import Session
from typing import Optional
from zeep.client import Client, Settings  # type:ignore
from zeep.transports import Transport


class ClientFluig:
    def __init__(
        self,
        wsdl_url: str,
        client_soap: Optional[Client] = None,
        settings: Optional[Settings] = None,
        verify_ssl: Optional[bool] = None,
    ) -> None:
        self._URL_WSDL = wsdl_url
        self._client_soap = client_soap
        self._settings = settings or Settings(strict=False)  # type:ignore
        self.__is_check_ssl = verify_ssl or None

    @property
    def soap_intance(self) -> Client:
        if self._client_soap is None and self.__is_check_ssl is None:
            session = Session()
            session.verify = False
            self._client_soap = Client(
                wsdl=self._URL_WSDL,
                settings=self._settings,
                transport=Transport(session),
            )

        else:
            self._client_soap = Client(wsdl=self._URL_WSDL, settings=self._settings)

        return self._client_soap

    def get_element_in_xml(self, element: str):
        client = self.soap_intance
        return client.get_type(element)
