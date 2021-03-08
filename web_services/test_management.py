from zeep import Client


class TestManagementWebService:
    def __init__(self, web_service_factory, server_prefix):
        self.web_service_factory = web_service_factory
        self.client = Client(server_prefix + 'TestManagementWebService?wsdl')

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
        :return:
        """
        self.client.service.setTestSteps(workitem_uri, test_steps)

    def create_test_run_with_title(self, project, id, title, template):
        """
        Create a new Test Run
        :param project: The Project the Test Run will be created in
        :param id: The Id of the Test Run to be created in
        :param title: The title of the Test Run to be created. The template title is used when null
        :param template: The template used to create the Test Run
        :return: The URI of the created Test Run
        """
        self.client.service.createTestRunWithTitle(project, id, title, template)
