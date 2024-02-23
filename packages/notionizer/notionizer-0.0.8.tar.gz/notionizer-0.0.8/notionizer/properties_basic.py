from notionizer.functions import from_rich_text_array_to_plain_text, from_plain_text_to_rich_text_array, pdir

from notionizer.object_adt import MutableProperty, ListObject, ImmutableProperty
from notionizer.object_basic import NotionBaseObject

from typing import Dict
from typing import Tuple
from typing import Any
from typing import Callable

from urllib import parse
_log = __import__('logging').getLogger(__name__)


class RichTextProperty(MutableProperty):
    """
    Specific object for richtext property.

    :: USAGE

    [1] print(db.title)
    'some title'

    [2] db.title = 'fixed title'
    ...

    """

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if type(value) == str:
            value = from_plain_text_to_rich_text_array(value)
        super().__set__(obj, value)


class TitleProperty(RichTextProperty):
    """
    Specific object for title of database.

    :: USAGE

    [1] print(db.title)
    'some title'

    [2] db.title = 'fixed title'
    ...

    """

    def __get__(self, obj, objtype=None):
        return from_rich_text_array_to_plain_text(getattr(obj, self.private_name))

    def __set__(self, obj, value):
        if type(value) == str:
            value = from_plain_text_to_rich_text_array(value)

        super().__set__(obj, value)

class IdProperty(ImmutableProperty):
    """
    Property for id of properties with decoding 'url'.
    """

    def __set__(self, obj: Any, value: Any) -> None:
        """
        set with decoding event
        :param obj:
        :param value:
        :return:
        """
        super().__set__(obj, parse.unquote(value))


class PropertyBaseObject(NotionBaseObject):
    """
    Basic Object for Data and Page Properties.
    """
    # to find which object is proper, uses '_type_defined' while assigning event.
    _type_defined = ''

    def __new__(cls, parent: Any, data: Dict[str, Any], parent_type: str, name: str, force_new: bool = False) \
            -> 'PropertyBaseObject':
        new_cls = super(PropertyBaseObject, cls)
        ins = new_cls.__new__(cls, data, force_new=force_new)  # type: ignore
        return ins

    def __init__(self, parent: Any, data: Dict[str, Any], parent_type: str, name: str, force_new: bool = False):
        """

        :param parent: PropertiesProperty
        :param data:
        :param parent_type:
        :param name:
        :param force_new:
        """
        self._parent: 'PropertiesProperty' = parent  # type: ignore
        self._parent_type = parent_type
        # dictionary for filter
        self._filter_body: Dict[str, Any] = dict()
        # page properties don't have 'name' property. This method assign '_name' property manually.
        self._name = name
        # self.name = name
        super().__init__(data)


class PagePropertyObject(PropertyBaseObject):
    """
    Basic Object for Data and Page Properties.
    """

    # to figure out which object is 'proper', uses '_type_defined' while assigning event.
    _type_defined = ''

    def __repr__(self) -> str:
        return f"<'{self.__class__.__name__}: {self._name}' at {hex(id(self))}>"

    def _update(self, property_name: str, data: Dict[str, Any]) -> None:
        self._parent._update(self._name, {property_name: data})
        # self._parent._update(self.name, {property_name: data})

    def get_value(self):

        value = getattr(self, self.type)

        if hasattr(value, 'keys'):
            if 'name' in value:
                # _log.info(f"{self}, {self.type}, {value.keys()}")
                return value['name'].replace(u'\xa0', u' ')
            else:
                # _log.info(f"{self}, {self.type}, {value}")
                # 빈 값에 대한 리턴 처리
                # return value
                return ''

        elif isinstance(value, (list, ListObject)):
            result = []
            for e in value:
                if hasattr(e, '__getitem__') and 'name' in e:
                    result.append(e['name'].replace(u'\xa0', u' '))
                elif hasattr(e, 'name') and e.name == 'relation':
                    result.append(e['id'])
                elif hasattr(e, 'name'):
                    result.append(e.name.replace(u'\xa0', u' '))
                else:
                    result.append(e)
            return tuple(result)
        else:
            # _log.info(f"{self}, {self.type}, {value}")
            return value


class DbPropertyObject(PropertyBaseObject):
    """
    Basic Object for Data and Page Properties.
    """
    # to find which object is proper, uses '_type_defined' while assigning event.
    _type_defined = ''
    _mutable = False

    id = IdProperty()
    name = MutableProperty()
    type = MutableProperty()
    _input_validation: Tuple[Callable[[Any], Any], ...] = tuple()

    def _update(self, property_name: str, data: Dict[str, Any]) -> None:
        if property_name == 'type':
            property_type = data
            self._parent._update(self.name, {property_name: property_type, property_type: {}})
        else:
            self._parent._update(self.name, {property_name: data})

    def _convert_to_update(self, value: Any) -> Dict[str, Any]:
        """
        convert value to update object form.

        to make some more specific, 'inheritance' should overide this method.

        ex) some_number_property._convert_to_update(123):
            return {'number': 123}

        :param value: nay of type
        :return: dictionary
        """
        return {self._type_defined: value}

    def __repr__(self) -> str:
        return f"<'{self.__class__.__name__}: {self.name}' at {hex(id(self))}>"

    def __lt__(self, other):
        raise Exception(f"Property '{self.type}' type does not support '__lt__' method")

    def __le__(self, other):
        raise Exception(f"Property '{self.type}' type does not support '__le__' method")

    def __eq__(self, other):
        raise Exception(f"Property '{self.type}' type does not support '__eq__' method")

    # !=
    def __ne__(self, other):
        raise Exception(f"Property '{self.type}' type does not support '__ne__' method")

    def __gt__(self, other):
        raise Exception(f"Property '{self.type}' type does not support '__gt__' method")

    def __ge__(self, other):
        raise Exception(f"Property '{self.type}' type does not support '__ge__' method")

    def __contains__(self, item):
        raise Exception(f"Property '{self.type}' type does not support '__contains__' method")

    def __and__(self, item):
        raise Exception(f"Property '{self.type}' type does not support '__and__' method")

    def __or__(self, item):
        raise Exception(f"Property '{self.type}' type does not support '__or__' method")
