

from datetime import date, time


class Comment:
    """
    Class comment
    """
    def __init__(self, comment):
        self.parent = None

        self._answers = []
        self._index = comment.id
        self._title = comment.title if comment.title else ""
        self._text = comment.text.content if comment.text else ""
        self._date = date(comment.created.year, comment.created.month, comment.created.day)
        self._time = time(comment.created.hour, comment.created.minute, comment.created.second)
        self._author = comment.author.name

        self._parent_uri = comment.parentCommentURI

    def link(self, *answers) -> None:
        """
        Method used to linked a list of comment to the current comment (answers)
        :param answers: Answers to be linked to the comment
        :return: None
        """
        for answer in answers:
            if answer:
                answer.parent = self
                self.answers.append(answer)

    @property
    def index(self) -> str:
        """
        Property used to get the id of the comment
        :return: id of the comment
        """
        return self._index

    @property
    def title(self) -> str:
        """
        Property used to get the title of the comment
        :return: title of the comment
        """
        return self._title

    @property
    def date(self) -> date:
        """
        Property used to get the date of the comment
        :return: date of the comment
        """
        return self._date

    @property
    def time(self) -> time:
        """
        Property used to get the time of the comment
        :return: time of the comment
        """
        return self._time

    @property
    def author(self) -> str:
        """
        Property used to get the author of the comment
        :return: author of the comment
        """
        return self._author

    @property
    def text(self) -> str:
        """
        Property used to get the text of the comment
        :return: text of the comment
        """
        return self._text

    @property
    def parent_uri(self) -> str:
        """
        Property used to get the parent_uri of the comment
        :return: parent_uri of the comment
        """
        return self._parent_uri

    @property
    def answers(self) -> []:
        """
        Property used to get the answers of the comment
        :return: answers of the comment
        """
        return self._answers

    @property
    def is_master_comment(self) -> bool:
        """
        Property used to know if the comment is a master one (source of a discussion)
        :return: True if comment is master one, else False
        """
        return not bool(self.parent)


class CommentsTree:
    """
    Class CommentTree
    """
    def __init__(self, workitem):
        """
        Class init
        :param workitem: Workitem which contains the comments to be ordered
        """
        self._comments = {}

        # Create the comments tree
        if workitem.comments:
            for comment in workitem.comments.Comment:
                self.__add(comment, workitem)

    def __getitem__(self, comment):
        return self._comments[comment]

    def __get_comment(self, comment) -> Comment:
        """
        Method used to get a comment if it exists or create it
        :param comment: Polarion comment object
        :return: Existing or created comment
        """
        if comment.id not in self._comments:
            self._comments[comment.id] = Comment(comment)
        return self._comments[comment.id]

    def __get_child(self, comment, answer) -> Comment or None:
        """
        Method used to get answers of comment
        :param comment: Comment considered as parent
        :param answer: Comment considered as potential answer
        :return: Answer if answer, else None
        """
        answer = self.__get_comment(answer)
        if comment.uri == answer.parent_uri:
            return answer
        return None

    def __add(self, comment, workitem) -> None:
        """
        Method used to create links between comment and other comments of a workitem
        :param comment: Comment considered as parent on wich answers will be added
        :param workitem: Workitem which contains the comments to be linked
        :return: None
        """
        self.__get_comment(comment).link(*(self.__get_child(comment, answer) for answer in workitem.comments.Comment))

    def get_master_comments(self) -> [Comment] or []:
        """
        Method used to get the list of master comments (sources of discussion)
        :return: List of master comments if exist, else empty list
        """
        master_comments = []
        for unused_index, comment in self._comments.items():
            if comment.is_master_comment:
                master_comments.append(comment)
        return master_comments

    def get_answers(self, index, level=0):
        """
        (Recursive) Method used to get discussion fill with a level corresponding to each comment
        :param index: Index of the comment
        :param level: Current level of the comment
        :return: Comment list with corresponding level
        """
        if not self._comments[index].answers:
            comments_list = [(self._comments[index], level)]
        else:
            comments_list = [(self._comments[index], level)]
            for answer in self._comments[index].answers:
                comments_list = comments_list + self.get_answers(answer.index, level+1)
        return comments_list
