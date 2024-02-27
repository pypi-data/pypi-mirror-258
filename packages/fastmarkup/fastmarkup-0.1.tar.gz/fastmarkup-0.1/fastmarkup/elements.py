from fastmarkup.components import HtmlComponent
from typing import Optional, Dict, Any


def merge_kwargs(
        kwargs: Dict[Any, Any],
        classname: Optional[str] = None,
        classlist: Optional[Dict[str, bool]] = None,
        for_: Optional[str] = None,
        id: Optional[str] = None,
        style: Optional[str] = None,
):
    if classname is not None:
        kwargs['classname'] = classname
    if classlist is not None:
        kwargs['classlist'] = classlist
    if id is not None:
        kwargs['id'] = id
    if style is not None:
        kwargs['style'] = style
    if for_ is not None:
        kwargs['for_'] = for_
    return kwargs


def a(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Together with its href attribute, creates a hyperlink to web pages, files, email addresses, locations within the current page, or anything else a URL can address.
    '''
    return HtmlComponent('a', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def abbr(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents an abbreviation or acronym.
    '''
    return HtmlComponent('abbr', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def acronym(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Allows authors to clearly indicate a sequence of characters that compose an acronym or abbreviation for a word.
    '''
    return HtmlComponent('acronym', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def address(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Indicates that the enclosed HTML provides contact information for a person or people, or for an organization.
    '''
    return HtmlComponent('address', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def animate(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('animate', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def animateMotion(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('animateMotion', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def animateTransform(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('animateTransform', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def area(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines an area inside an image map that has predefined clickable areas. An image map allows geometric areas on an image to be associated with hyperlink.
    '''
    return HtmlComponent('area', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def article(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a self-contained composition in a document, page, application, or site, which is intended to be independently distributable or reusable (e.g., in syndication). Examples include a forum post, a magazine or newspaper article, a blog entry, a product card, a user-submitted comment, an interactive widget or gadget, or any other independent item of content.
    '''
    return HtmlComponent('article', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def aside(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a portion of a document whose content is only indirectly related to the document's main content. Asides are frequently presented as sidebars or call-out boxes.
    '''
    return HtmlComponent('aside', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def audio(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to embed sound content in documents. It may contain one or more audio sources, represented using the src attribute or the source element: the browser will choose the most suitable one. It can also be the destination for streamed media, using a MediaStream.
    '''
    return HtmlComponent('audio', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def b(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to draw the reader's attention to the element's contents, which are not otherwise granted special importance. This was formerly known as the Boldface element, and most browsers still draw the text in boldface. However, you should not use <b> for styling text or granting importance. If you wish to create boldface text, you should use the CSS font-weight property. If you wish to indicate an element is of special importance, you should use the strong element.
    '''
    return HtmlComponent('b', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def base(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies the base URL to use for all relative URLs in a document. There can be only one such element in a document.
    '''
    return HtmlComponent('base', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def bdi(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Tells the browser's bidirectional algorithm to treat the text it contains in isolation from its surrounding text. It's particularly useful when a website dynamically inserts some text and doesn't know the directionality of the text being inserted.
    '''
    return HtmlComponent('bdi', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def bdo(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Overrides the current directionality of text, so that the text within is rendered in a different direction.
    '''
    return HtmlComponent('bdo', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def big(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Renders the enclosed text at a font size one level larger than the surrounding text (medium becomes large, for example). The size is capped at the browser's maximum permitted font size.
    '''
    return HtmlComponent('big', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def blockquote(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Indicates that the enclosed text is an extended quotation. Usually, this is rendered visually by indentation. A URL for the source of the quotation may be given using the cite attribute, while a text representation of the source can be given using the <cite> element.
    '''
    return HtmlComponent('blockquote', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def body(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    represents the content of an HTML document. There can be only one such element in a document.
    '''
    return HtmlComponent('body', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def br(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Produces a line break in text (carriage-return). It is useful for writing a poem or an address, where the division of lines is significant.
    '''
    return HtmlComponent('br', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def button(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    An interactive element activated by a user with a mouse, keyboard, finger, voice command, or other assistive technology. Once activated, it performs an action, such as submitting a form or opening a dialog.
    '''
    return HtmlComponent('button', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def canvas(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Container element to use with either the canvas scripting API or the WebGL API to draw graphics and animations.
    '''
    return HtmlComponent('canvas', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def caption(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies the caption (or title) of a table.
    '''
    return HtmlComponent('caption', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def center(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Displays its block-level or inline contents centered horizontally within its containing element.
    '''
    return HtmlComponent('center', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def circle(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('circle', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def cite(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to mark up the title of a cited creative work. The reference may be in an abbreviated form according to context-appropriate conventions related to citation metadata.
    '''
    return HtmlComponent('cite', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def clipPath(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('clipPath', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def clippath(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('clippath', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def code(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Displays its contents styled in a fashion intended to indicate that the text is a short fragment of computer code. By default, the content text is displayed using the user agent's default monospace font.
    '''
    return HtmlComponent('code', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def col(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a column within a table and is used for defining common semantics on all common cells. It is generally found within a <colgroup> element.
    '''
    return HtmlComponent('col', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def colgroup(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a group of columns within a table.
    '''
    return HtmlComponent('colgroup', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def content(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    An obsolete part of the Web Components suite of technologies—was used inside of Shadow DOM as an insertion point, and wasn't meant to be used in ordinary HTML. It has now been replaced by the <slot> element, which creates a point in the DOM at which a shadow DOM can be inserted. Consider using <slot> instead.
    '''
    return HtmlComponent('content', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def cursor(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('cursor', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def data(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Links a given piece of content with a machine-readable translation. If the content is time- or date-related, the<time> element must be used.
    '''
    return HtmlComponent('data', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def datalist(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Contains a set of <option> elements that represent the permissible or recommended options available to choose from within other controls.
    '''
    return HtmlComponent('datalist', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def dd(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Provides the description, definition, or value for the preceding term (<dt>) in a description list (<dl>).
    '''
    return HtmlComponent('dd', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def defs(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('defs', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def del_(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a range of text that has been deleted from a document. This can be used when rendering \"track changes\" or source code diff information, for example. The <ins> element can be used for the opposite purpose: to indicate text that has been added to the document.
    '''
    return HtmlComponent('del_', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def desc(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('desc', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def details(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Creates a disclosure widget in which information is visible only when the widget is toggled into an \"open\" state. A summary or label must be provided using the <summary> element.
    '''
    return HtmlComponent('details', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def dfn(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to indicate the term being defined within the context of a definition phrase or sentence. The ancestor <p> element, the <dt>/<dd> pairing, or the nearest section ancestor of the <dfn> element, is considered to be the definition of the term.
    '''
    return HtmlComponent('dfn', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def dialog(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a dialog box or other interactive component, such as a dismissible alert, inspector, or subwindow.
    '''
    return HtmlComponent('dialog', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def dir(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Container for a directory of files and/or folders, potentially with styles and icons applied by the user agent. Do not use this obsolete element; instead, you should use the <ul> element for lists, including lists of files.
    '''
    return HtmlComponent('dir', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def div(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    The generic container for flow content. It has no effect on the content or layout until styled in some way using CSS (e.g., styling is directly applied to it, or some kind of layout model like flexbox is applied to its parent element).
    '''
    return HtmlComponent('div', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def dl(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a description list. The element encloses a list of groups of terms (specified using the <dt> element) and descriptions (provided by <dd> elements). Common uses for this element are to implement a glossary or to display metadata (a list of key-value pairs).
    '''
    return HtmlComponent('dl', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def dt(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies a term in a description or definition list, and as such must be used inside a <dl> element. It is usually followed by a <dd> element; however, multiple <dt> elements in a row indicate several terms that are all defined by the immediate next <dd> element.
    '''
    return HtmlComponent('dt', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def ellipse(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('ellipse', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def em(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Marks text that has stress emphasis. The <em> element can be nested, with each nesting level indicating a greater degree of emphasis.
    '''
    return HtmlComponent('em', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def embed(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Embeds external content at the specified point in the document. This content is provided by an external application or other source of interactive content such as a browser plug-in.
    '''
    return HtmlComponent('embed', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feBlend(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feBlend', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feColorMatrix(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feColorMatrix', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feComponentTransfer(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feComponentTransfer', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feComposite(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feComposite', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feConvolveMatrix(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feConvolveMatrix', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feDiffuseLighting(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feDiffuseLighting', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feDisplacementMap(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feDisplacementMap', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feDistantLight(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feDistantLight', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feDropShadow(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feDropShadow', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feFlood(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feFlood', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feFuncA(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feFuncA', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feFuncB(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feFuncB', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feFuncG(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feFuncG', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feFuncR(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feFuncR', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feGaussianBlur(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feGaussianBlur', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feImage(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feImage', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feMerge(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feMerge', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feMergeNode(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feMergeNode', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feMorphology(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feMorphology', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feOffset(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feOffset', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def fePointLight(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('fePointLight', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feSpecularLighting(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feSpecularLighting', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feSpotLight(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feSpotLight', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feTile(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feTile', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def feTurbulence(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('feTurbulence', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def fieldset(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to group several controls as well as labels (<label>) within a web form.
    '''
    return HtmlComponent('fieldset', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def figcaption(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a caption or legend describing the rest of the contents of its parent <figure> element.
    '''
    return HtmlComponent('figcaption', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def figure(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents self-contained content, potentially with an optional caption, which is specified using the <figcaption> element. The figure, its caption, and its contents are referenced as a single unit.
    '''
    return HtmlComponent('figure', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def filter(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('filter', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def font(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('font', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def footer(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a footer for its nearest ancestor sectioning content or sectioning root element. A <footer> typically contains information about the author of the section, copyright data, or links to related documents.
    '''
    return HtmlComponent('footer', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def foreignObject(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('foreignObject', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def form(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a document section containing interactive controls for submitting information.
    '''
    return HtmlComponent('form', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def frame(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a particular area in which another HTML document can be displayed. A frame should be used within a <frameset>.
    '''
    return HtmlComponent('frame', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def frameset(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to contain <frame> elements.
    '''
    return HtmlComponent('frameset', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def g(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('g', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def glyph(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('glyph', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def glyphRef(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('glyphRef', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def h1(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    '''
    return HtmlComponent('h1', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def h2(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    '''
    return HtmlComponent('h2', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def h3(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    '''
    return HtmlComponent('h3', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def h4(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    '''
    return HtmlComponent('h4', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def h5(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    '''
    return HtmlComponent('h5', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def h6(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    '''
    return HtmlComponent('h6', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def hatch(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('hatch', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def hatchpath(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('hatchpath', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def head(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Contains machine-readable information (metadata) about the document, like its title, scripts, and style sheets.
    '''
    return HtmlComponent('head', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def header(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents introductory content, typically a group of introductory or navigational aids. It may contain some heading elements but also a logo, a search form, an author name, and other elements.
    '''
    return HtmlComponent('header', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def hgroup(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a heading grouped with any secondary content, such as subheadings, an alternative title, or a tagline.
    '''
    return HtmlComponent('hgroup', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def hkern(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('hkern', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def hr(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a thematic break between paragraph-level elements: for example, a change of scene in a story, or a shift of topic within a section.
    '''
    return HtmlComponent('hr', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def html(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents the root (top-level element) of an HTML document, so it is also referred to as the root element. All other elements must be descendants of this element.
    '''
    return HtmlComponent('html', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def i(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a range of text that is set off from the normal text for some reason, such as idiomatic text, technical terms, and taxonomical designations, among others. Historically, these have been presented using italicized type, which is the original source of the <i> naming of this element.
    '''
    return HtmlComponent('i', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def iframe(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a nested browsing context, embedding another HTML page into the current one.
    '''
    return HtmlComponent('iframe', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def image(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('image', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def img(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Embeds an image into the document.
    '''
    return HtmlComponent('img', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def input(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to create interactive controls for web-based forms to accept data from the user; a wide variety of types of input data and control widgets are available, depending on the device and user agent. The <input> element is one of the most powerful and complex in all of HTML due to the sheer number of combinations of input types and attributes.
    '''
    return HtmlComponent('input', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def ins(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a range of text that has been added to a document. You can use the <del> element to similarly represent a range of text that has been deleted from the document.
    '''
    return HtmlComponent('ins', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def kbd(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a span of inline text denoting textual user input from a keyboard, voice input, or any other text entry device. By convention, the user agent defaults to rendering the contents of a <kbd> element using its default monospace font, although this is not mandated by the HTML standard.
    '''
    return HtmlComponent('kbd', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def label(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a caption for an item in a user interface.
    '''
    return HtmlComponent('label', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def legend(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a caption for the content of its parent <fieldset>.
    '''
    return HtmlComponent('legend', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def li(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents an item in a list. It must be contained in a parent element: an ordered list (<ol>), an unordered list (<ul>), or a menu (<menu>). In menus and unordered lists, list items are usually displayed using bullet points. In ordered lists, they are usually displayed with an ascending counter on the left, such as a number or letter.
    '''
    return HtmlComponent('li', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def line(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('line', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def linearGradient(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('linearGradient', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def lineargradient(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('lineargradient', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def link(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies relationships between the current document and an external resource. This element is most commonly used to link to CSS but is also used to establish site icons (both \"favicon\" style icons and icons for the home screen and apps on mobile devices) among other things.
    '''
    return HtmlComponent('link', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def main(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents the dominant content of the body of a document. The main content area consists of content that is directly related to or expands upon the central topic of a document, or the central functionality of an application.
    '''
    return HtmlComponent('main', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def map(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used with <area> elements to define an image map (a clickable link area).
    '''
    return HtmlComponent('map', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def mark(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents text which is marked or highlighted for reference or notation purposes due to the marked passage's relevance in the enclosing context.
    '''
    return HtmlComponent('mark', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def marker(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('marker', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def marquee(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to insert a scrolling area of text. You can control what happens when the text reaches the edges of its content area using its attributes.
    '''
    return HtmlComponent('marquee', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def mask(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('mask', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def math(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    The top-level element in MathML. Every valid MathML instance must be wrapped in it. In addition, you must not nest a second <math> element in another, but you can have an arbitrary number of other child elements in it.
    '''
    return HtmlComponent('math', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def menu(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    A semantic alternative to <ul>, but treated by browsers (and exposed through the accessibility tree) as no different than <ul>. It represents an unordered list of items (which are represented by <li> elements).
    '''
    return HtmlComponent('menu', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def menuitem(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a command that a user is able to invoke through a popup menu. This includes context menus, as well as menus that might be attached to a menu button.
    '''
    return HtmlComponent('menuitem', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def meta(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents metadata that cannot be represented by other HTML meta-related elements, like <base>, <link>, <script>, <style> and <title>.
    '''
    return HtmlComponent('meta', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def metadata(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('metadata', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def meter(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents either a scalar value within a known range or a fractional value.
    '''
    return HtmlComponent('meter', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def missing(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('missing', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def mpath(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('mpath', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def nav(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a section of a page whose purpose is to provide navigation links, either within the current document or to other documents. Common examples of navigation sections are menus, tables of contents, and indexes.
    '''
    return HtmlComponent('nav', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def nobr(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Prevents the text it contains from automatically wrapping across multiple lines, potentially resulting in the user having to scroll horizontally to see the entire width of the text.
    '''
    return HtmlComponent('nobr', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def noembed(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    An obsolete, non-standard way to provide alternative, or \"fallback\", content for browsers that do not support the embed element or do not support the type of embedded content an author wishes to use. This element was deprecated in HTML 4.01 and above in favor of placing fallback content between the opening and closing tags of an <object> element.
    '''
    return HtmlComponent('noembed', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def noframes(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Provides content to be presented in browsers that don't support (or have disabled support for) the <frame> element. Although most commonly-used browsers support frames, there are exceptions, including certain special-use browsers including some mobile browsers, as well as text-mode browsers.
    '''
    return HtmlComponent('noframes', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def noscript(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a section of HTML to be inserted if a script type on the page is unsupported or if scripting is currently turned off in the browser.
    '''
    return HtmlComponent('noscript', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def object(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents an external resource, which can be treated as an image, a nested browsing context, or a resource to be handled by a plugin.
    '''
    return HtmlComponent('object', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def ol(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents an ordered list of items — typically rendered as a numbered list.
    '''
    return HtmlComponent('ol', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def optgroup(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Creates a grouping of options within a <select> element.
    '''
    return HtmlComponent('optgroup', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def option(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to define an item contained in a select, an <optgroup>, or a <datalist> element. As such, <option> can represent menu items in popups and other lists of items in an HTML document.
    '''
    return HtmlComponent('option', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def output(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Container element into which a site or app can inject the results of a calculation or the outcome of a user action.
    '''
    return HtmlComponent('output', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def p(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a paragraph. Paragraphs are usually represented in visual media as blocks of text separated from adjacent blocks by blank lines and/or first-line indentation, but HTML paragraphs can be any structural grouping of related content, such as images or form fields.
    '''
    return HtmlComponent('p', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def param(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines parameters for an <object> element.
    '''
    return HtmlComponent('param', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def path(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('path', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def pattern(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('pattern', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def picture(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Contains zero or more <source> elements and one <img> element to offer alternative versions of an image for different display/device scenarios.
    '''
    return HtmlComponent('picture', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def plaintext(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Renders everything following the start tag as raw text, ignoring any following HTML. There is no closing tag, since everything after it is considered raw text.
    '''
    return HtmlComponent('plaintext', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def polygon(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('polygon', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def polyline(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('polyline', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def portal(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Enables the embedding of another HTML page into the current one to enable smoother navigation into new pages.
    '''
    return HtmlComponent('portal', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def pre(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents preformatted text which is to be presented exactly as written in the HTML file. The text is typically rendered using a non-proportional, or monospaced, font. Whitespace inside this element is displayed as written.
    '''
    return HtmlComponent('pre', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def progress(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.
    '''
    return HtmlComponent('progress', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def q(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Indicates that the enclosed text is a short inline quotation. Most modern browsers implement this by surrounding the text in quotation marks. This element is intended for short quotations that don't require paragraph breaks; for long quotations use the <blockquote> element.
    '''
    return HtmlComponent('q', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def radialGradient(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('radialGradient', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def radialgradient(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('radialgradient', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def rb(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to delimit the base text component of a ruby annotation, i.e. the text that is being annotated. One <rb> element should wrap each separate atomic segment of the base text.
    '''
    return HtmlComponent('rb', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def rect(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('rect', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def rp(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to provide fall-back parentheses for browsers that do not support the display of ruby annotations using the <ruby> element. One <rp> element should enclose each of the opening and closing parentheses that wrap the <rt> element that contains the annotation's text.
    '''
    return HtmlComponent('rp', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def rt(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies the ruby text component of a ruby annotation, which is used to provide pronunciation, translation, or transliteration information for East Asian typography. The <rt> element must always be contained within a <ruby> element.
    '''
    return HtmlComponent('rt', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def rtc(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Embraces semantic annotations of characters presented in a ruby of <rb> elements used inside of <ruby> element. <rb> elements can have both pronunciation (<rt>) and semantic (<rtc>) annotations.
    '''
    return HtmlComponent('rtc', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def ruby(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents small annotations that are rendered above, below, or next to base text, usually used for showing the pronunciation of East Asian characters. It can also be used for annotating other kinds of text, but this usage is less common.
    '''
    return HtmlComponent('ruby', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def s(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Renders text with a strikethrough, or a line through it. Use the <s> element to represent things that are no longer relevant or no longer accurate. However, <s> is not appropriate when indicating document edits; for that, use the del and ins elements, as appropriate.
    '''
    return HtmlComponent('s', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def samp(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used to enclose inline text which represents sample (or quoted) output from a computer program. Its contents are typically rendered using the browser's default monospaced font (such as Courier or Lucida Console).
    '''
    return HtmlComponent('samp', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def script(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('script', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def search(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a part that contains a set of form controls or other content related to performing a search or filtering operation.
    '''
    return HtmlComponent('search', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def section(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a generic standalone section of a document, which doesn't have a more specific semantic element to represent it. Sections should always have a heading, with very few exceptions.
    '''
    return HtmlComponent('section', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def select(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a control that provides a menu of options.
    '''
    return HtmlComponent('select', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def set(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('set', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def shadow(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    An obsolete part of the Web Components technology suite that was intended to be used as a shadow DOM insertion point. You might have used it if you have created multiple shadow roots under a shadow host. Consider using <slot> instead.
    '''
    return HtmlComponent('shadow', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def slot(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Part of the Web Components technology suite, this element is a placeholder inside a web component that you can fill with your own markup, which lets you create separate DOM trees and present them together.
    '''
    return HtmlComponent('slot', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def small(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents side-comments and small print, like copyright and legal text, independent of its styled presentation. By default, it renders text within it one font size smaller, such as from small to x-small.
    '''
    return HtmlComponent('small', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def solidcolor(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('solidcolor', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def source(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies multiple media resources for the picture, the audio element, or the video element. It is a void element, meaning that it has no content and does not have a closing tag. It is commonly used to offer the same media content in multiple file formats in order to provide compatibility with a broad range of browsers given their differing support for image file formats and media file formats.
    '''
    return HtmlComponent('source', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def span(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    A generic inline container for phrasing content, which does not inherently represent anything. It can be used to group elements for styling purposes (using the class or id attributes), or because they share attribute values, such as lang. It should be used only when no other semantic element is appropriate. <span> is very much like a div element, but div is a block-level element whereas a <span> is an inline-level element.
    '''
    return HtmlComponent('span', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def stop(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('stop', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def strike(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Places a strikethrough (horizontal line) over text.
    '''
    return HtmlComponent('strike', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def strong(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Indicates that its contents have strong importance, seriousness, or urgency. Browsers typically render the contents in bold type.
    '''
    return HtmlComponent('strong', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def style(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('style', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def sub(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies inline text which should be displayed as subscript for solely typographical reasons. Subscripts are typically rendered with a lowered baseline using smaller text.
    '''
    return HtmlComponent('sub', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def summary(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies a summary, caption, or legend for a details element's disclosure box. Clicking the <summary> element toggles the state of the parent <details> element open and closed.
    '''
    return HtmlComponent('summary', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def sup(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Specifies inline text which is to be displayed as superscript for solely typographical reasons. Superscripts are usually rendered with a raised baseline using smaller text.
    '''
    return HtmlComponent('sup', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def svg(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('svg', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def switch(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('switch', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def symbol(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('symbol', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def table(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents tabular data — that is, information presented in a two-dimensional table comprised of rows and columns of cells containing data.
    '''
    return HtmlComponent('table', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def tbody(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Encapsulates a set of table rows (<tr> elements), indicating that they comprise the body of the table (<table>).
    '''
    return HtmlComponent('tbody', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def td(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a cell of a table that contains data. It participates in the table model.
    '''
    return HtmlComponent('td', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def template(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    A mechanism for holding HTML that is not to be rendered immediately when a page is loaded but may be instantiated subsequently during runtime using JavaScript.
    '''
    return HtmlComponent('template', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def text(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('text', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def textPath(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('textPath', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def textarea(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a multi-line plain-text editing control, useful when you want to allow users to enter a sizeable amount of free-form text, for example, a comment on a review or feedback form.
    '''
    return HtmlComponent('textarea', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def tfoot(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a set of rows summarizing the columns of the table.
    '''
    return HtmlComponent('tfoot', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def th(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a cell as a header of a group of table cells. The exact nature of this group is defined by the scope and headers attributes.
    '''
    return HtmlComponent('th', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def thead(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a set of rows defining the head of the columns of the table.
    '''
    return HtmlComponent('thead', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def time(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a specific period in time. It may include the datetime attribute to translate dates into machine-readable format, allowing for better search engine results or custom features such as reminders.
    '''
    return HtmlComponent('time', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def title(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('title', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def tr(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Defines a row of cells in a table. The row's cells can then be established using a mix of <td> (data cell) and <th> (header cell) elements.
    '''
    return HtmlComponent('tr', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def track(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Used as a child of the media elements, audio and video. It lets you specify timed text tracks (or time-based data), for example to automatically handle subtitles. The tracks are formatted in WebVTT format (.vtt files)—Web Video Text Tracks.
    '''
    return HtmlComponent('track', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def tref(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('tref', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def tspan(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('tspan', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def tt(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Creates inline text which is presented using the user agent default monospace font face. This element was created for the purpose of rendering text as it would be displayed on a fixed-width display such as a teletype, text-only screen, or line printer.
    '''
    return HtmlComponent('tt', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def u(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a span of inline text which should be rendered in a way that indicates that it has a non-textual annotation. This is rendered by default as a simple solid underline but may be altered using CSS.
    '''
    return HtmlComponent('u', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def ul(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents an unordered list of items, typically rendered as a bulleted list.
    '''
    return HtmlComponent('ul', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def use(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('use', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def var(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents the name of a variable in a mathematical expression or a programming context. It's typically presented using an italicized version of the current typeface, although that behavior is browser-dependent.
    '''
    return HtmlComponent('var', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def video(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Embeds a media player which supports video playback into the document. You can also use <video> for audio content, but the audio element may provide a more appropriate user experience.
    '''
    return HtmlComponent('video', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def view(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('view', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def vkern(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
     SVG Element
    '''
    return HtmlComponent('vkern', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def wbr(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Represents a word break opportunity—a position within text where the browser may optionally break a line, though its line-breaking rules would not otherwise create a break at that location.
    '''
    return HtmlComponent('wbr', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))


def xmp(
    *args,
    classname: Optional[str] = None,
    classlist: Optional[Dict[str, bool]] = None,
    style: Optional[str] = None,
    id: Optional[str] = None,
    for_: Optional[str] = None,
    **kwargs
):
    '''
    Renders text between the start and end tags without interpreting the HTML in between and using a monospaced font. The HTML2 specification recommended that it should be rendered wide enough to allow 80 characters per line.
    '''
    return HtmlComponent('xmp', args, merge_kwargs(kwargs, classname, classlist, for_, id, style))
