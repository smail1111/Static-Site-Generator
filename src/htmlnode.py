class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not Implemented")
    
    def props_to_html(self):
        return " " + " ".join(
            list(
                map(lambda attribute: f'{attribute}="{self.props[attribute]}"', 
                self.props)
                )
            ) if self.props else ""

    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        return f"HTMLNode(Tag= {self.tag}, Value= {self.value}, Children= {self.children} Attributes={self.props_to_html()})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No Value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"HTMLNode(Tag= {self.tag}, Value= {self.value}, Attributes={self.props_to_html()})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("No Tag")
        if self.children is None:
            raise ValueError("No Children")
        
        children_html = "".join(list(
                map(lambda child: child.to_html(), self.children)
                )
            )
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode(Tag= {self.tag}, Children= {self.children} Attributes={self.props_to_html()})"