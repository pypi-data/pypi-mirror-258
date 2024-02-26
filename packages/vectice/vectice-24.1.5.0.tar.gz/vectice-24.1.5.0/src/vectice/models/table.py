from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


class Table:
    """Represents a table structure containing custom metadata that can be logged inside Vectice.

    To document custoom metadata into Vectice, you need to wrap it as a Vectice Table
    This class facilitates wrapping metadata a in a tabular format, which can then be logged to Vectice iterations for documentation.
    Once logged, the tabular metadata becomes accessible within the application.

    NOTE: **IMPORTANT INFORMATION**
        It's important to note that this metadata will be available in its raw form within Vectice, meaning that the information will be stored as-is, without additional processing or transformation.

    """

    def __init__(
        self,
        dataframe: DataFrame,
        name: str | None = None,
    ):
        """Wrap a Table.

        A Vectice Table is a wrapped pandas dataframe in a tabular format, which can then be logged to a Vectice iteration.

        Parameters:
            dataframe: The pandas dataframe to be wrapped as table.
            name: The name of the table for future reference.

        """
        self._name = name or f"table {datetime.now()}"
        self._dataframe = dataframe

    @property
    def name(self) -> str:
        """The table's name.

        Returns:
            The table name.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set the table's name.

        Parameters:
            name: The name of the table.
        """
        self._name = name

    @property
    def dataframe(self) -> DataFrame:
        """The Table's data.

        Returns:
            The table.
        """
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe: DataFrame):
        """Set the table's pandas dataframe.

        Parameters:
            dataframe: The pandas dataframe to be displayed as table.
        """
        self._dataframe = dataframe
