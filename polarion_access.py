from web_services.tracker import TrackerWebService
from web_services.project import ProjectWebService
from web_services.test_management import TestManagementWebService

from zeep import Client
from zeep.plugins import HistoryPlugin


class PolarionAccess:
    """
        Polarion
        Class used to open web service factory instance on Polarion
    """
    def __init__(self, hostname):

        self._hostname = hostname

        temp_wsdl_prefix_address = 'http://%s/polarion/ws/services/' % hostname

        self._session_header_element = None
        self._history = HistoryPlugin()
        self._session = Client(wsdl=temp_wsdl_prefix_address + 'SessionWebService?wsdl', plugins=[self._history])

        self._tracker = TrackerWebService(self, temp_wsdl_prefix_address)
        self._project = ProjectWebService(self, temp_wsdl_prefix_address)
        self._test_management = TestManagementWebService(self, temp_wsdl_prefix_address)

    def log_in(self, login, password):
        self._session.service.logIn(login, password)
        root_tree = self._history.last_received['envelope'].getroottree()
        self._session_header_element = root_tree.find('.//{http://ws.polarion.com/session}sessionID')

        self._tracker.client.set_default_soapheaders([self._session_header_element])
        self._project.client.set_default_soapheaders([self._session_header_element])
        self._test_management.client.set_default_soapheaders([self._session_header_element])

    @property
    def tracker(self):
        return self._tracker

    @property
    def project(self):
        return self._project

    @property
    def test_management(self):
        return self._test_management

    def end_session(self):
        """
        Terminates the current session
        :return: -
        """
        self._session.service.endSession()

    def begin_transaction(self):
        """
        Starts a explicit transaction for the current session. Usually transactions are started and committed for each
        call to the webservice, but if a transaction has been started explicitly it also has to be terminated using
        endTransaction.
        :return: -
        """
        self._session.service.beginTransaction()

    def end_transaction(self, rollback):
        """
        Ends the explicit transaction of the current session by either commit or rollback.
        :param rollback: if true the transaction is rolled back otherwise it is  committed (boolean)
        :return: -
        """
        self._session.service.endTransaction(rollback)