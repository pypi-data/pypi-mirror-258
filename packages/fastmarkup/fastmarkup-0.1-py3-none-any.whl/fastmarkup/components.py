
from dataclasses import dataclass
import html as htmllib
from re import escape
from typing import Any, Callable, Dict, Generic, List, Literal, Optional, Tuple, Type, TypeVar, Union


python_keywords = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'finally',
    'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
    'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
]

T = TypeVar('T')


class Component:
    def render(self) -> str:
        return ''


class FragmentComponent(Component):
    def __init__(self, children: Tuple) -> None:
        self.children = []
        self.__add(children)

    def __add(self, children: Tuple):
        for child in children:
            if isinstance(child, tuple):
                self.children.append(FragmentComponent(child))
            else:
                self.children.append(child)

    def __call__(self, *args: Union[Component, str] | Tuple[Union[Component, str]]):
        self.__add(args)
        return self

    def render(self):
        content = '\n'.join(
            child.render() if isinstance(child, Component) else str(child) for child in self.children
        )
        return content


@dataclass
class AttributeContext:
    tag: Optional[str]
    attribute: str
    value: Any
    omit: bool
    classes: List[str]


class BaseProcessor:
    def process_attribute(self, context: AttributeContext):
        pass


class ClassNameProcessor(BaseProcessor):
    def process_attribute(self, context: AttributeContext):
        if context.attribute == 'classname':
            context.classes.extend(str(context.value).split(' '))
            context.omit = True


class UnderscoreProcessor(BaseProcessor):
    def process_attribute(self, context: AttributeContext):
        context.attribute = context.attribute.replace(
            '__', ':').replace('_', '-')


class KeywordsProcessor(BaseProcessor):
    def process_attribute(self, context: AttributeContext):
        if context.attribute == 'class_':
            context.classes.extend(str(context.value).split(' '))
            context.omit = True
        elif context.attribute.endswith('_') and context.attribute[:-1] in python_keywords:
            context.attribute = context.attribute[:-1]


class ClassListProcessor(BaseProcessor):
    def process_attribute(self, context: AttributeContext):
        if context.attribute == 'classlist' and isinstance(context.value, dict):
            context.omit = True
            for classname, value in context.value.items():
                if value:
                    context.classes.append(classname)


default_processors = [
    KeywordsProcessor(),
    ClassNameProcessor(),
    ClassListProcessor(),
    UnderscoreProcessor(),
]


class JavaScriptExpression:
    def __init__(self, script: str) -> None:
        self.script = script


class HtmlComponent(Component):
    def __init__(self, tag: Optional[str], children: Tuple, attributes: dict[str, Any]) -> None:
        self.children: List[Any] = []
        self.tag = tag
        self.attributes = attributes
        self.__add(children)
        self.processors: List[BaseProcessor] = default_processors

    def __html__(self):
        return self.render()

    def __add(self, children: Tuple):
        for child in children:
            if isinstance(child, tuple):
                self.children.append(FragmentComponent(child))
            else:
                self.children.append(child)

    def __call__(self, *args: Any | Tuple[Any]):
        self.__add(args)
        return self

    def render(self):
        attributes = ''
        classes: List[str] = []
        for key, value in self.attributes.items():
            context = AttributeContext(self.tag, key, value, False, classes)
            for procesor in self.processors:
                procesor.process_attribute(context)
            if not context.omit:
                if (isinstance(context.value, bool) and context.value == False) or context.value == None:
                    continue
                attributes += context.attribute
                if isinstance(context.value, bool) and context.value == True:
                    attributes += '\n'
                else:
                    if isinstance(context.value, JavaScriptExpression):
                        attributes += f'="{context.value.script}"\n'
                    else:
                        attributes += f'="{htmllib.escape(str(context.value))}"\n'
        if len(classes) > 0:
            attributes += f'class="{" ".join(classes)}"\n'

        content = '\n'.join(
            child.render() if isinstance(child, Component) else
            child.script if isinstance(child, JavaScriptExpression) else
            htmllib.escape(str(child or ''))
            for child in self.children
        )
        return f'<{self.tag} {attributes}>{content}</{self.tag}>' if self.tag else f'{content}'


class ForEachComponent(Component, Generic[T]):
    def __init__(self, items: List[T]) -> None:
        self.items = items
        self.children: List[Any] = []

    def __call__(self, each: Callable[[T, int], Any | Tuple[Any]]):
        index = 0
        for item in self.items:
            child = each(item, index)
            if isinstance(child, (list, tuple)):
                self.children.extend(child)
            else:
                self.children.append(child)
            index += 1
        return self

    def render(self):
        content = '\n'.join(
            child.render() if isinstance(child, Component) else str(child) for child in self.children
        )
        return content


class WhenComponent(Component):
    def __init__(self, condition: Any) -> None:
        self.condition = condition
        self.children: List[Component] = []

    def __add(self, children: Tuple):
        for child in children:
            if isinstance(child, tuple):
                self.children.append(FragmentComponent(child))
            else:
                self.children.append(child)

    def __call__(self, *args: Any | Tuple[Any]):
        if self.condition:
            self.__add(args)
        return self

    def render(self):
        if len(self.children) > 0:
            return '\n'.join(
                child.render() if isinstance(child, Component) else str(child) for child in self.children
            )
        return ''


def foreach(items: List[T]):
    return ForEachComponent(items)


def when(value: Any):
    return WhenComponent(value)


def fragment(*args):
    return FragmentComponent(args)


def dynamic(component: str, *args, **kwargs):
    return HtmlComponent(component, args, kwargs)


def el(tag: str, *args, **kwargs):
    return HtmlComponent(tag, args, kwargs)


def js(script: str):
    return JavaScriptExpression(script)
