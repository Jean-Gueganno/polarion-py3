from zeep import Client
from zeep.plugins import HistoryPlugin


class SessionWebService:
    """
    Class SessionWebService
    This class gives access to SessionWebService.wsdl description file
    """

    def __init__(self, polarion_access, server_prefix):
        self._history = HistoryPlugin()
        self._polarion_access = polarion_access
        self.client = Client(wsdl=server_prefix + 'SessionWebService?wsdl', plugins=[self._history])
        self._session_header_element = None

    def log_in(self, username: str, password: str) -> None:
        """
        Method used to log into Polarion using defined user account and password.
        :param username: Username used to log in
        :param password: Password used to log in
        :return: None
        """
        self.client.service.logIn(username, password)

        root_tree = self._history.last_received['envelope'].getroottree()

        self._session_header_element = root_tree.find('.//{http://ws.polarion.com/session}sessionID')
        self.client.set_default_soapheaders([self._session_header_element])

    @property
    def session_header_element(self):
        """
        Property used to get the current session header element
        :return: Current session header element
        """
        return self._session_header_element

    def end_session(self) -> None:
        """
        Method used to terminates the current session
        :return: None
        """
        self.client.service.endSession()

    def has_subject(self) -> bool:
        """
        Checks if a user is logged-in for the current session.
        :return: True if user is logged in, else False
        """
        return self.client.service.hasSubject()

    def begin_transaction(self) -> None:
        """
        Method used to start an explicit transaction for the current session. Usually transactions are started and
        committed for each call to the webservice, but if a transaction has been started explicitly it also has to be
        terminated using endTransaction.
        :return: None
        """
        self.client.service.beginTransaction()

    def end_transaction(self, rollback: bool) -> None:
        """
        Method used to end the explicit transaction of the current session by either commit or rollback.
        :param rollback: if true the transaction is rolled back otherwise it is  committed (boolean)
        :return: None
        """
        self.client.service.endTransaction(rollback)
