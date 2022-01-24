from zeep import Client


class TrackerWebService:
    """
    Class TrackerWebService
    This class gives access to TrackerWebService.wsdl description file
    """

    def __init__(self, polarion_access, server_prefix, session_header_element):
        self._polarion_access = polarion_access
        self.client = Client(server_prefix + 'TrackerWebService?wsdl')
        self.client.settings.strict = False
        self.client.set_default_soapheaders([session_header_element])
        self.client.settings.strict = False

    def create_workitem(self, project_id: str, type_id: str, title: str, description_content: str = ""):
        """
        Function used to create a new workitem
        :param project_id: project id (string)
        :param type_id: workitem type id(string)
        :param title: workitem title (string)
        :param description_content: workitem description (string)
        :return: URI of created work item
        """
        project = self._polarion_access.project.client.service.getProject(project_id)
        wi_type = self.client.type_factory('ns2').EnumOptionId(id=type_id)
        description = self.client.type_factory('ns1').Text(type='text/html',
                                                           content=description_content.replace("\n", "<br>"),
                                                           contentLossy=False)

        workitem = self.client.type_factory('ns2').WorkItem(project=project,
                                                            type=wi_type,
                                                            title=title,
                                                            description=description)

        # Create the work item
        return self.client.service.createWorkItem(workitem)

    def query_workitems(self, query: str, sort: str = 'id', fields: [str] = None) -> []:
        """
        Function used to get a list of workitems using Polarion query (can be found using filter option in Polarion)
        :param query:  (string) the lucene query to be used
        :param sort: (string) the field to be used for sorting
        :param fields: (string[]) the keys of the fields that should be filled
        :return: the list of workitems
        """
        if fields is None:
            fields = ['type', 'id', 'status', 'description', 'linkedWorkItems']
        return self.client.service.queryWorkItems(query, sort, fields)

    def get_workitem_by_id(self, project_id: str, workitem_id: str):
        """
        Function used to get a workitem using project and workitem IDs
        :param project_id: the id of the project that contains the workitem to get
        :param workitem_id: the id of the work item to get
        :return: Workitem requested
        """
        return self.client.service.getWorkItemById(project_id, workitem_id)

    def get_workitem_by_uri(self, workitem_uri: str):
        """
        Function used to get a workitem using its uri
        :param workitem_uri: the uri of the work item to get
        :return: Workitem requested
        """
        return self.client.service.getWorkItemByUri(workitem_uri)

    def get_custom_field(self, workitem_uri, custom_field_key):
        """
        Function used to get a custom field of a work item
        :param workitem_uri: the URI of the work item to get the custom field from
        :param custom_field_key: the key of the custom field
        :return: Custom field as an object
        """
        return self.client.service.getCustomField(workitem_uri, custom_field_key)

    def get_enum_control_key(self, project_id, enum_id):
        return self.client.service.getEnumControlKeyForId(project_id, enum_id)

    def add_comment(self, workitem_uri: str, title: str, comment: str) -> None:
        """
        Function used to set a comment on dedicated workitem
        :param workitem_uri: URI of workitem
        :param title: Comment tile
        :param comment: Comment description (can be HTML content)
        :return: None
        """
        # convert comment to Text type
        comment_text = self.client.type_factory('ns1').Text(type='text/html',
                                                            content=comment,
                                                            contentLossy=False)

        self.client.service.addComment(workitem_uri, title, comment_text)

    def set_status(self, project_id: str, workitem_id: str, value: str) -> None:
        """
        Function used to set workitem status to specific value (workflow)
        :param project_id: Workitem project id
        :param workitem_id: Workitem id
        :param value: Status value (Polarion id of the status)
        :return:
        """
        workitem = self.get_workitem_by_id(project_id, workitem_id)
        workitem.status.id = value

        self.client.service.updateWorkItem(workitem)

    def set_severity(self, project_id: str, workitem_id: str, value: str) -> None:
        """
        Mthod used to set severity of a workitem to a specific value
        :param project_id: Project ID of the workitem
        :param workitem_id: Workitem if
        :param value: Value to set
        :return: None
        """
        enum_option = self.client.type_factory('ns2').EnumOptionId(id=value)

        workitem = self.get_workitem_by_id(project_id, workitem_id)
        workitem.severity = enum_option

        self.client.service.updateWorkItem(workitem)

    def set_custom_field(self, workitem_uri, custom_field_key, value):
        """
        Function used to get a custom field of a work item
        :param workitem_uri: the URI of the work item to get the custom field from
        :param custom_field_key: the key of the custom field
        :param value: Value to set
        :return:
        """
        enum_option = self.client.type_factory('ns2').EnumOptionId(id=value)
        custom_field = self.client.type_factory('ns2').CustomField(key=custom_field_key,
                                                                   parentItemURI=workitem_uri,
                                                                   value=enum_option)
        return self.client.service.setCustomField(custom_field)

    def add_linked_item_by_id(self, project_id, workitem_id, linked_project_id, linked_workitem_id, role):
        """
        Adds a linked work item
        :param project_id: the ID of the project where the workitem to add the link to is
        :param workitem_id: the ID of the work item to add the link to
        :param linked_project_id: the ID of the project where the target work item the link points to is
        :param linked_workitem_id: the ID of the target work item the link points to
        :param role: the role of the link to add
        :return: True if link has been added, else False
        """
        # Translate string into polarion type
        new_role = self.client.type_factory('ns2').EnumOptionId(id=role)

        # Get the two concerned items
        workitem = self.get_workitem_by_id(project_id, workitem_id)
        linked_workitem = self.get_workitem_by_id(linked_project_id, linked_workitem_id)

        # Set the link
        # noinspection PyProtectedMember
        return self.client.service.addLinkedItem(workitem._uri, linked_workitem._uri, new_role)

    def add_linked_item(self, workitem_uri: str, linked_workitem_uri: str, role: str) -> bool:
        """
        Adds a linked work item
        :param workitem_uri: the ID of the work item to add the link to
        :param linked_workitem_uri: the ID of the target work item the link points to
        :param role: the role of the link to add
        :return: True if link has been added, else False
        """
        # Translate string into polarion type
        new_role = self.client.type_factory('ns2').EnumOptionId(id=role)

        # Set the link
        return self.client.service.addLinkedItem(workitem_uri, linked_workitem_uri, new_role)

    def remove_linked_item(self, workitem_uri, linked_item_uri, role) -> bool:
        """
        Function used to remove an existing link between two workitems
        :param workitem_uri: URI of workitems
        :param linked_item_uri: URI of the link workitem
        :param role: Link role to remove between the two workitems
        :return: True if link has been removed, else False
        """
        # Translate string into polarion type
        new_role = self.client.type_factory('ns2').EnumOptionId(id=role)
        return self.client.service.removeLinkedItem(workitem_uri, linked_item_uri, new_role)

    def get_document(self, project_id: str, location: str):
        """
        Function used to retrieve the document on the given location.
        :param project_id: Project ID of the document
        :param location: Location of the document in the project. Format : SPACE/DOCUMENT_ID (i.e : 2x_Control/20_Zone)
        :return: The requested document
        """
        return self.client.service.getModuleByLocation(project_id, location)

    def get_documents(self, project_id: str, location: str) -> object or [object] or None:
        """
        Method used to get all documents on the given location relative to the "modules" folder of the given project.
        :param project_id: Project ID of the documents
        :param location: The serialized location relative to the "modules" folder
        :return: One document (if only one document in the folder)
                 Array of document (if more than one document in the folder)
                 None (if no document in the folder)
        """
        return self.client.service.getModules(project_id, location)

    def get_document_by_uri(self, document_uri):
        """
        Method used to get a document using its URI
        :param document_uri: URI of the document
        :return: The requested document
        """
        return self.client.service.getModuleByUri(document_uri)

    def get_documents_sub_folder(self, project_id: str, location: str) -> [str] or None:
        """
        Method used to get the sub-folders of a given location relative to the "documents" folder.
        :param project_id: Project ID of the folder
        :param location: Location relative to the "documents" folder.
        :return: Array of serialized locations (if exist)
                 None (if no location)
        """
        return self.client.service.getModulesSubFolders(project_id, location)

    def set_document_custom_field(self,
                                  document_uri: str,
                                  custom_field_key: str,
                                  custom_field_value: str or int) -> None:
        """
        Method used to update a specific custom field of a document
        WARNING, this method can only be used to set or update str/int custom field, not enumerated or rich text custom
                 fields
        :param document_uri: URI of the document
        :param custom_field_key: Custom field key identifier
        :param custom_field_value: Custom field value to apply
        :return: None
        """
        custom_field = self.client.type_factory('ns2').Custom(key=custom_field_key, value=custom_field_value)

        document = self.get_document_by_uri(document_uri)
        document.customFields.Custom.append(custom_field)

        self.client.service.updateModule(document)

    def generate_workitem_history_by_id(self, project_id: str, workitem_id: str, ignored_fields: [str] = "",
                                        field_order: [str] = ""):
        """
        Method used to generate a specific history for a workitem using its id
        :param project_id: Project ID of the workitem
        :param workitem_id: Workitem ID
        :param ignored_fields: Fields to ignore
        :param field_order: Field used to sort the history
        :return: Change history
        """
        workitem = self.get_workitem_by_id(project_id, workitem_id)
        changes = self.client.service.generateHistory(workitem.uri, ignored_fields, field_order)
        return changes

    def generate_workitem_history_by_uri(self, workitem_uri: str, ignored_fields: [str] = "", field_order: [str] = ""):
        """
        Method used to generate a specific history for a workitem using its uri
        :param workitem_uri: Workitem URI
        :param ignored_fields: Fields to ignore
        :param field_order: Field used to sort the history
        :return: Change history
        """
        changes = self.client.service.generateHistory(workitem_uri, ignored_fields, field_order)
        return changes
