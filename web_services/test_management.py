
from zeep import Client, xsd


class TestManagementWebService:
    """
    Class TestManagementWebService
    This class gives access to TestManagementWebService.wsdl description file
    """

    def __init__(self, web_service_factory, server_prefix, session_header_element):
        self.web_service_factory = web_service_factory
        self.client = Client(server_prefix + 'TestManagementWebService?wsdl')
        self.client.set_default_soapheaders([session_header_element])

    def factory_create(self, class_reference):
        """
        Create an object with which has a specific class reference
        :param class_reference: class reference (can be found in wsdl)
        :return: corresponding class
        """
        return self.client.type_factory(class_reference)

    def get_test_steps(self, workitem_uri):
        """
        Gets the TestSteps of WI with given URI
        :param workitem_uri: the URI of the work item to get
        :return: the test steps of WI with given URI
        """
        return self.client.service.getTestSteps(workitem_uri)

    def set_test_steps(self, workitem_uri, test_steps):
        """
        Adds Test Steps to WI with given URI (add operation). If WI already has Test Steps, they will be completely
        replaced (update operation). If the testSteps parameter is null, the content of the Test Steps field will be
        emptied (delete operation).
        :param workitem_uri: the SubterraURI of the item to set the WI
        :param test_steps: an array containing an entry for each step
        :return: None
        """
        self.client.service.setTestSteps(workitem_uri, test_steps)

    def create_test_run_with_title(self, project, test_run_id, title, template):
        """
        Create a new Test Run
        :param project: The Project the Test Run will be created in
        :param test_run_id: The Id of the Test Run to be created in
        :param title: The title of the Test Run to be created. The template title is used when null
        :param template: The template used to create the Test Run
        :return: None
        """
        self.client.service.createTestRunWithTitle(project, test_run_id, title, template)

    def get_test_run(self, project, test_run_id):
        """
        Create a new Test Run
        :param project: The Project the Test Run
        :param test_run_id: The Id of the Test Run to find
        :return: The URI of the created Test Run
        """
        return self.client.service.getTestRunById(project, test_run_id)

    def get_test_case_records(self, test_run_uri, test_case_uri):
        """
        Create a new Test Run
        :param test_run_uri:
        :param test_case_uri:
        :return: The URI of the created Test Run
        """
        return self.client.service.getTestCaseRecords(test_run_uri, test_case_uri)

    def add_test_record(self,
                        test_run_uri,
                        test_case_uri,
                        test_result_id: str,
                        test_comment: str,
                        executed_by_uri,
                        executed,
                        duration: float,
                        defect_uri=xsd.SkipValue):
        """
        Create a new Test Record
        :param test_run_uri:
        :param test_case_uri:
        :param test_result_id:
        :param test_comment:
        :param executed_by_uri:
        :param executed:
        :param duration:
        :param defect_uri
        :return: None
        """

        self.client.service.addTestRecord(test_run_uri,
                                          test_case_uri,
                                          test_result_id,
                                          test_comment,
                                          executed_by_uri,
                                          executed,
                                          duration,
                                          defect_uri)

    def update_test_record(self,
                           test_case_uri,
                           index: int,
                           test_result_id: str,
                           test_comment: str,
                           executed_by_uri,
                           executed,
                           duration: float,
                           defect_uri=xsd.SkipValue):
        """

        :param test_case_uri:
        :param index:
        :param test_result_id:
        :param test_comment:
        :param executed_by_uri:
        :param executed:
        :param duration:
        :param defect_uri:
        :return:
        """

        self.client.service.updateTestRecord(test_case_uri,
                                             index,
                                             test_result_id,
                                             test_comment,
                                             executed_by_uri,
                                             executed,
                                             duration,
                                             defect_uri)

    def execute_test(self, test_run_uri, records):
        """

        :param test_run_uri:
        :param records:
        :return:
        """
        self.client.service.executeTest(test_run_uri, records)
