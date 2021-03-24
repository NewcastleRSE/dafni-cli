from typing import Optional, List

from dafni_cli.datasets.dataset_metadata import DatasetMetadata
from dafni_cli.utils import check_key_in_dict
from dafni_cli.api.datasets_api import get_latest_dataset_metadata


class DatasetVersionHistory:
    """Class for processing Dataset Version History,

    Methods:
        __init__(jwt (str), metadata (dict)): DatasetVersionHistory constructor
        set_details_from_dict(metadata (dict)): Function to set the class details from a given dict
        process_version_history(jwt (str), dataset (dict)): Iterates through all versions and outputs details

    Attributes:
        jwt (str): Users DAFNI JWT
        dataset_id (str): Dataset ID
        versions (List[dict]): List of associated Version dicts
        version_ids (List[str]): List of Version IDs
    """

    def __init__(self, jwt: Optional[str] = None, metadata: Optional[dict] = None):
        """DatasetVersionHistory constructor

        Args:
            jwt (Optional[str], optional): Users DAFNI JWT. Defaults to None.
            metadata (Optional[dict], optional): Dataset Metadata response. Defaults to None.
        """
        self.jwt = jwt
        self.dataset_id = None
        self.versions = None
        self.version_ids = None

        if metadata:
            self.set_details_from_dict(metadata)

    def set_details_from_dict(self, metadata: dict):
        """Helper function to populate the DatasetVersionHistory details
        based on a given DAFNI Dataset Metadata response

        Args:
            metadata (dict): DAFNI Dataset Metadata response
        """
        self.dataset_id = check_key_in_dict(
            metadata, ["version_history", "dataset_uuid"]
        )
        self.versions = check_key_in_dict(
            metadata, ["version_history", "versions"], default=[]
        )
        self.version_ids = [
            check_key_in_dict(version, ["version_uuid"], default=None)
            for version in self.versions
        ]

    def process_version_history(self):
        """Function iterates through all Version History ID's,
        retrieves the associated Dataset Metadata, and outputs the Version details
        to the command line
        """
        for version_id in self.version_ids:
            metadata = get_latest_dataset_metadata(
                self.jwt, self.dataset_id, version_id
            )
            dataset_meta = DatasetMetadata(metadata, version_id=version_id)
            dataset_meta.output_version_details()