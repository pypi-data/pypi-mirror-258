class init:
    def __init__(self) -> None:
        pass

    def _get_data_recursive(self, element):
        if len(element) == 0:
            return element.text.strip() if element.text else None
        else:
            data = {}
            for child in element:
                data[child.tag] = self._get_data_recursive(child)
            return data