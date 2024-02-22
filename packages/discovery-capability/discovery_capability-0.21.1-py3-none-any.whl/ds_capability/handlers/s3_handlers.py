import threading
from io import StringIO, BytesIO
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.feather as feather
from pyarrow import csv
import os
from ds_core.handlers.abstract_handlers import AbstractSourceHandler, AbstractPersistHandler, HandlerFactory
from ds_core.handlers.abstract_handlers import ConnectorContract

__author__ = 'Darryl Oatridge'


class S3SourceHandler(AbstractSourceHandler):
    """ An Amazon AWS S3 source handler.

        URI Format:
            uri = 's3://<bucket>[/<path>]/<filename.ext>'

        Restrictions:
            - This does not use the AWS S3 Multipart Upload and is limited to 5GB files
    """

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the connector_contract dictionary

        Extra Parameters in the ConnectorContract kwargs:
            - region_name (optional) session region name
            - profile_name (optional) session shared credentials file profile name
        """
        # required module import
        self.boto3 = HandlerFactory.get_module('boto3')
        self.botocore_exceptions = HandlerFactory.get_module('botocore.exceptions')
        super().__init__(connector_contract)
        cc_params = connector_contract.kwargs
        cc_params.update(connector_contract.query)  # Update kwargs with those in the uri query
        region_name = cc_params.pop('region_name', 'us-east-2')
        aws_access_key_id = cc_params.pop('aws_access_key_id', os.environ.get('AWS_ACCESS_KEY_ID'))
        aws_secret_access_key = cc_params.pop('aws_secret_access_key', os.environ.get('AWS_SECRET_ACCESS_KEY'))
        aws_session_token = cc_params.pop('aws_session_token', os.environ.get('AWS_SESSION_TOKEN'))
        profile_name = cc_params.pop('profile_name', None)
        self._session = self.boto3.Session(region_name=region_name, aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key, profile_name=profile_name,
                                      aws_session_token=aws_session_token)
        self._file_state = 0
        self._changed_flag = True
        self._lock = threading.Lock()

    def supported_types(self) -> list:
        """ The source types supported with this module"""
        return ['parquet', 'csv', 'tsv', 'txt', 'json', 'pickle']

    def exists(self) -> bool:
        """ Returns True is the file exists

        Extra Parameters in the ConnectorContract kwargs:
            - s3_list_params: (optional) a dictionary of additional s3 parameters directly passed to 'list_objects_v2'

        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The S3 Source Connector Contract has not been set correctly")
        _cc = self.connector_contract
        if not isinstance(_cc, ConnectorContract):
            raise ValueError("The Python Source Connector Contract has not been set correctly")
        cc_params = _cc.kwargs
        cc_params.update(_cc.query)  # Update kwargs with those in the uri query
        s3_list_params = cc_params.pop('s3_list_params', {})
        if _cc.schema not in ['s3']:
            raise ValueError("The Connector Contract Schema has not been set correctly.")
        s3_client = self._session.client(_cc.schema)
        response = s3_client.list_objects_v2(Bucket=_cc.netloc, **s3_list_params)
        for obj in response.get('Contents', []):
            if obj['Key'] == _cc.path[1:]:
                return True
        return False

    def has_changed(self) -> bool:
        """ returns if the file has been modified

            - s3_get_params: (optional) a dictionary of additional s3 client parameters directly passed to 'get_object'
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The S3 Source Connector Contract has not been set correctly")
        _cc = self.connector_contract
        if not isinstance(_cc, ConnectorContract):
            raise ValueError("The Python Source Connector Contract has not been set correctly")
        cc_params = _cc.kwargs
        cc_params.update(_cc.query)  # Update kwargs with those in the uri query
        # pop all the extra params
        s3_get_params = cc_params.pop('s3_get_params', {})
        if _cc.schema not in ['s3']:
            raise ValueError("The Connector Contract Schema has not been set correctly.")
        s3_client = self._session.client(_cc.schema)
        try:
            s3_object = s3_client.get_object(Bucket=_cc.netloc, Key=_cc.path[1:], **s3_get_params)
        except self.botocore_exceptions.ClientError as e:
            code = e.response["Error"]["Code"]
            raise ConnectionError("Failed to retrieve the object from region '{}', bucket '{}' "
                                  "Key '{}' with error code '{}'".format(self._session.region_name, _cc.netloc,
                                                                         _cc.path[1:], code))
        state = s3_object.get('LastModified', 0)
        if state != self._file_state:
            self._changed_flag = True
            self._file_state = state
        return self._changed_flag

    def reset_changed(self, changed: bool = False):
        """ manual reset to say the file has been seen. This is automatically called if the file is loaded"""
        changed = changed if isinstance(changed, bool) else False
        self._changed_flag = changed

    def load_canonical(self, **kwargs) -> pa.Table:
        """Loads the canonical dataset, returning a Pandas DataFrame. This method utilises the pandas
        'pd.read_' methods and directly passes the kwargs to these methods.

        Extra Parameters in the ConnectorContract kwargs:
            - file_type: (optional) the type of the source file. if not set, inferred from the file extension
                            by default json files load as dict, to load as pandas use read_params '{as_dataframe: True}
            - encoding: (optional) the encoding of the s3 object body. Default 'utf-8'
            - s3_get_params: (optional) a dictionary of additional s3 client parameters directly passed to 'get_object'
            - read_params: (optional) value pair dict of parameters to pass to the read methods. Underlying
                           read methods the parameters are passed to are all pandas 'read_*', e.g. pd.read_csv

        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The S3 Source Connector Contract has not been set correctly")
        _cc = self.connector_contract
        if not isinstance(_cc, ConnectorContract):
            raise ValueError("The Python Source Connector Contract has not been set correctly")
        _, _, _ext = _cc.address.rpartition('.')
        cc_params = _cc.kwargs
        cc_params.update(_cc.query)  # Update kwargs with those in the uri query
        cc_params.update(kwargs)     # Update with any passed though the call
        # pop all the extra params
        encoding = cc_params.pop('encoding', 'utf-8')
        file_type = cc_params.pop('file_type', _ext if len(_ext) > 0 else 'parquet')
        s3_get_params = cc_params.pop('s3_get_params', {})
        if file_type.lower() not in self.supported_types():
            raise ValueError("The file type {} is not recognised. "
                             "Set file_type parameter to a recognised source type".format(file_type))
        # session
        if _cc.schema not in ['s3']:
            raise ValueError("The Connector Contract Schema has not been set correctly.")
        s3_client = self._session.client(_cc.schema)
        try:
            s3_object = s3_client.get_object(Bucket=_cc.netloc, Key=_cc.path[1:], **s3_get_params)
        except self.botocore_exceptions.ClientError as e:
            code = e.response["Error"]["Code"]
            raise ConnectionError("Failed to retrieve the object from region '{}', bucket '{}' "
                                  "Key '{}' with error code '{}'".format(self._session.region_name, _cc.netloc,
                                                                         _cc.path[1:], code))
        resource_body = s3_object['Body'].read()
        with self._lock:
            if file_type.lower() in ['parquet', 'pq', 'pqt']:
                results = pq.read_table(BytesIO(resource_body), **cc_params)
            elif file_type.lower() in ['feather']:
                return feather.read_table(BytesIO(resource_body), **cc_params)
            elif file_type.lower() in ['csv', 'tsv', 'txt']:
                parse_options = csv.ParseOptions(**cc_params)
                results = csv.read_csv(BytesIO(resource_body), parse_options=parse_options)
            else:
                raise LookupError('The source format {} is not currently supported'.format(file_type))
        s3_client.close()
        return results


class S3PersistHandler(S3SourceHandler, AbstractPersistHandler):
    """ An Amazon AWS S3 source handler.

        URI Format:
            uri = 's3://<bucket>[/<path>]/<filename.ext>'

        Restrictions:
            - This does not use the AWS S3 Multipart Upload and is limited to 5GB files
    """

    def persist_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ persists either the canonical dataset.

        Extra Parameters in the ConnectorContract kwargs:
            - file_type: (optional) the type of the source file. if not set, inferred from the file extension
            - s3_put_params: (optional) a dictionary of additional s3 client parameters directly passed to 'get_object'
            - write_params: (optional) value pair dict of parameters to pass to the write methods - pandas.to_csv,
                              pandas.to_json, pickle.dump and parquet.Table.from_pandas
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        _uri = self.connector_contract.address
        return self.backup_canonical(uri=_uri, canonical=canonical, **kwargs)

    def backup_canonical(self, canonical: pa.Table, uri: str, **kwargs) -> bool:
        """ persists the canonical dataset as a backup to the specified URI resource. Note that only the
        address is taken from the URI and all other attributes are taken from the ConnectorContract

        Extra Parameters in the ConnectorContract kwargs:
            - file_type: (optional) the type of the source file. if not set, inferred from the file extension
            - s3_put_params: (optional) value pair dict of parameters to pass to the Boto3 put_object method
            - write_params: (optional) value pair dict of parameters to pass to the write methods - pandas.to_csv,
                              pandas.to_json, pickle.dump and parquet.Table.from_pandas
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The S3 Source Connector Contract has not been set correctly")
        _cc = self.connector_contract
        if not isinstance(_cc, ConnectorContract):
            raise ValueError("The Python Source Connector Contract has not been set correctly")
        schema, bucket, path = _cc.parse_address_elements(uri=uri)
        _, _, _ext = path.rpartition('.')
        cc_params = kwargs if isinstance(kwargs, dict) else _cc.kwargs
        cc_params.update(_cc.parse_query(uri=uri))
        # pop all the extra params
        s3_put_params = cc_params.pop('s3_put_params', _cc.kwargs.get('put_object_kw', {}))
        write_params = cc_params.pop('write_params', _cc.kwargs.get('write_kw', {}))
        file_type = cc_params.pop('file_type', _cc.kwargs.get('file_type', _ext if len(_ext) > 0 else 'pkl'))
        if _cc.schema not in ['s3']:
            raise ValueError("The Connector Contract Schema has not been set correctly.")
        s3_client = self._session.client(_cc.schema)
        # csv
        if file_type.lower() in ['csv', 'tsv', 'txt']:
            byte_obj = BytesIO()
            with self._lock:
                csv.write_csv(canonical, byte_obj)
                s3_client.put_object(Bucket=bucket, Key=path[1:], Body=byte_obj.getvalue(), **s3_put_params)
        # parquet
        elif file_type.lower() in ['parquet', 'pq', 'pqt']:
            byte_obj = BytesIO()
            with self._lock:
                pq.write_table(canonical, byte_obj)
                s3_client.put_object(Bucket=bucket, Key=path[1:], Body=byte_obj.getvalue(), **s3_put_params)
        elif file_type.lower() in ['feather']:
            byte_obj = BytesIO()
            with self._lock:
                feather.write_feather(canonical, byte_obj)
                s3_client.put_object(Bucket=bucket, Key=path[1:], Body=byte_obj.getvalue(), **s3_put_params)
                return True
        else:
            raise LookupError('The source format {} is not currently supported for write'.format(file_type))
        s3_client.close()
        return True

    def remove_canonical(self) -> bool:
        """ removes the URI named resource

        Extra Parameters in the ConnectorContract kwargs:
            - s3_del_params: (optional) value pair dict of parameters to pass to the Boto3 delete_object method
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The S3 Source Connector Contract has not been set correctly")
        _cc = self.connector_contract
        if not isinstance(_cc, ConnectorContract):
            raise ValueError("The Python Source Connector Contract has not been set correctly")
        cc_params = _cc.kwargs
        cc_params.update(_cc.query)  # Update kwargs with those in the uri query
        # pop all the extra params
        s3_del_params = cc_params.pop('s3_put_params', _cc.kwargs.get('put_object_kw', {}))
        if _cc.schema not in ['s3']:
            raise ValueError("The Connector Contract Schema has not been set correctly.")
        s3_client = self._session.client(_cc.schema)
        response = s3_client.response = s3_client.delete_object(Bucket=_cc.netloc, Key=_cc.path[1:], **s3_del_params)
        if response.get('RequestCharged') is None:
            return False
        return True
