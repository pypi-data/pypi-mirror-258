from notionizer.object_adt import DictionaryObject, ListObject, ImmutableProperty, MutableProperty
from notionizer.exception import NotionApiPropertyException
from notionizer.http_request import HttpRequest
from typing import Any
from typing import Optional
from typing import Dict
from typing import Tuple
from typing import List

_log = __import__('logging').getLogger(__name__)


notion_object_class: Dict[str, Any] = {}


def create_notion_object_class(cls: Any, mro_tuple: Optional[Tuple[Any]] = None,
                               namespace: Optional[Dict[str, Any]] = None, force_new: bool = False) -> Any:
    """
    Create new 'NotionBaseObject' class. Check the name of 'cls'. If not exist,
    create and return. After created, the 'NotionBaseObject' has own descriptors. If exists, returns already created one
    with descriptors assigned.

    :param cls: 'NotionBaseObject' itself or 'subclass' of it.
    :param mro_tuple: if it is defined, replace this.
    :param namespace: if it is defined, replace this.
    :param force_new: if True, generate new object even it exists.
    :return: new or created class.
    """
    new_cls: Any = None
    cls_name = cls.__name__

    if not namespace:
        namespace = dict()

    if (cls_name in notion_object_class) and (not force_new):
        new_cls = notion_object_class[cls_name]
    else:
        if not mro_tuple:
            mro_tuple = (cls,)
        # _log.debug(f"{cls_name} {'(force_new)' if force_new else ''}")
        new_cls = type(cls_name, mro_tuple, namespace)
        notion_object_class[cls_name] = new_cls

    return new_cls


class NotionBaseObject(object):
    """
    'NotionBaseObject' set properties as 'descriptor' or 'specific object' and assigns value.
    """

    def __new__(cls, data: Dict[str, Any], force_new: bool = False) -> 'NotionBaseObject':
        """
        construct 'NotionBaseObject' class.

        before assign the object and property, '__new__' method set the proper descriptors.
        :param data:
        """
        _log.debug(f"{cls}")
        new_cls = create_notion_object_class(cls, force_new=force_new)

        for k, v in data.items():
            if k not in dir(new_cls):
                set_proper_descriptor(new_cls, k, v)

        super_cls = super(NotionBaseObject, new_cls)
        notion_ins: 'NotionBaseObject' = super_cls.__new__(new_cls)
        return notion_ins

    def __init__(self, data: Dict[str, Any], *args: List[Any]):
        """
        assign object and property to instance.
        :param data:
        """
        _log.debug(f"{self} data: {data}")
        for k, v in data.items():
            setattr(self, k, v)

    def __str__(self):
        return f"<'{self.__class__.__name__}'>"

    def __repr__(self):
        return f"<'{self.__class__.__name__}' at {hex(id(self))}>"


class UserBaseObject(NotionBaseObject):
    """
    User Object.
    """

    object = ImmutableProperty()
    id = ImmutableProperty()
    name = ImmutableProperty()

    def __str__(self) -> str:
        user_name = ''
        try:
            user_name = f": {self.name}"
        except AttributeError:
            return self.__repr__()
        symbol = f"<'User{user_name}'>"
        return symbol

    def __repr__(self) -> str:
        user_name = ''
        user_id = ''
        try:
            user_id = f" at '{self.id}'"
            user_name = f": {self.name}"
        except AttributeError:
            pass
        symbol = f"<'User{user_name}'{user_id}>"
        return symbol


class ObjectProperty(ImmutableProperty):
    """
    ObjectProperty which inherits 'ImmutableProperty'.
    """

    def __set__(self, owner: Any, value: Dict[str, Any]) -> None:
        obj = DictionaryObject(self.public_name, owner, value)
        super().__set__(owner, obj)


class ArrayProperty(ImmutableProperty):
    """
    ArrayProperty which inherits 'ImmutableProperty'.
    """

    def __init__(self, owner: Any=None, name: Optional[str] = '', mutable: bool=False):
        self.mutable = mutable
        super().__init__(owner=owner, name=str(name))

    def __set__(self, owner: Any, value: List[Any]) -> None:

        obj = ListObject(self.public_name, owner, value, mutable=self.mutable)

        super().__set__(owner, obj)


class ArrayPropertyMutable(MutableProperty):
    """
    ArrayProperty which inherits 'MutableProperty'.
    """

    def __init__(self, owner: Any=None, name: Optional[str] = '', mutable: bool=False):
        self.mutable = mutable
        super().__init__(owner=owner, name=str(name))

    def __set__(self, owner: Any, value: List[Any]) -> None:

        obj = ListObject(self.public_name, owner, value, mutable=self.mutable)

        super().__set__(owner, obj)


class RichTextProperty(ArrayProperty):
    pass

def set_proper_descriptor(cls: Any, key: str, value: Any) -> None:
    """
    check the value type and assign property with proper descriptor.
    (only descriptor, not value)

    :param cls: object
    :param key: str
    :param value: primitive, rich_text,  dictionary, list
    :return: None
    """

    obj: Any

    if type(value) in [str, bool, int, float] or (value is None):
        setattr(cls, key, ImmutableProperty(cls, key))

    elif key == 'rich_text':
        obj = RichTextProperty(cls, key, mutable=True)
        # _log.debug(f"rich_text, {cls}, {key}: {value}")
        setattr(cls, key, obj)

    elif type(value) == dict:
        obj = ObjectProperty(cls, key)
        setattr(cls, key, obj)

    elif type(value) == list:
        obj = ArrayProperty(cls, key)
        setattr(cls, key, obj)
    else:
        raise NotionApiPropertyException(f"could not assign proper descriptor: '{type(value)}'")



class NotionUpdateObject(NotionBaseObject):
    """
    'NotionUpdateObject' overrides '_update' method for updating and refreshing itself.
    """
    _instances: Dict[str, Any] = {}

    _api_url: str
    id: ImmutableProperty

    def __new__(cls, request: HttpRequest, data: Dict[str, Any], instance_id: Optional[str] = None
                , **kwargs) -> 'NotionUpdateObject':
        """
        construct 'NotionUpdateObject' class.

        check 'key' value and if instance is exist, reuse instance with renewed namespace.
        :param request:
        :param data:
        :param instance_id:
        """

        _log.debug(" ".join(map(str, ('NotionUpdateObject:', cls))))
        instance: 'NotionUpdateObject' = super(NotionUpdateObject, cls).__new__(cls, data)  # type: ignore

        # assign 'new namespace' with 'unassigned descriptors'.
        if instance_id:
            NotionUpdateObject._instances[instance_id].__dict__ = instance.__dict__
        else:
            # print(data)
            instance_id = str(data['id'])
            NotionUpdateObject._instances[instance_id] = instance

        return instance

    def __init__(self, request: HttpRequest, data: Dict[str, Any], instance_id: Optional[str] = None):
        """

        :param request:
        :param data:
        :param instance_id:
        """
        _log.debug(" ".join(map(str, ('NotionUpdateObject:', self))))
        self._request: HttpRequest = request
        super().__init__(data)

    def _update(self, property_name: str, contents: Dict[str, Any]) -> None:
        url = self._api_url + str(self.id)
        request, data = self._request.patch(url, {property_name: contents})
        # update property of object using 'id' value.
        cls: type(NotionUpdateObject) = type(self)  # type: ignore
        # update instance
        cls(request, data, instance_id=str(data['id']))


# class Listblock(ListObject):
#     pass

