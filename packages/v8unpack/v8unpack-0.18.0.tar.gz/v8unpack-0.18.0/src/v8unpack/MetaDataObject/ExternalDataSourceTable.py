from ..MetaDataObject.core.Container import Container


class ExternalDataSourceTable(Container):
    @classmethod
    def get_decode_header(cls, header_data):
        return header_data[0][1][1][1]
