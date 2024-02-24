from __future__ import annotations
import desbordante

__all__ = ["DataStats", "Default"]

class DataStats(desbordante.Algorithm):
    """
    Options:
    table: table processed by the algorithm
    is_null_equal_null: specify whether two NULLs should be considered equal
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    """
    def __init__(self) -> None: ...
    def get_all_statistics_as_string(self) -> str: ...
    def get_average(self, index: int) -> float | int | str:
        """
        Returns average value in the column if it's numeric.
        """
    def get_columns_with_all_unique_values(self) -> list[int]:
        """
        Get indices of columns where all values are distinct.
        """
    def get_columns_with_null(self) -> list[int]:
        """
        Get indices of columns which contain null value.
        """
    def get_corrected_std(self, index: int) -> float | int | str:
        """
        Returns corrected standard deviation of the column if it's numeric.
        """
    def get_geometric_mean(self, index: int) -> float | int | str:
        """
        Returns geometric mean of numbers in the column if it's numeric.
        """
    def get_kurtosis(self, index: int) -> float | int | str:
        """
        Returns kurtosis of the column if it's numeric.
        """
    def get_max(self, index: int) -> float | int | str:
        """
        Returns maximumin value of the column.
        """
    def get_mean_ad(self, index: int) -> float | int | str:
        """
        Returns mean absolute deviation of the column if it's numeric.
        """
    def get_median(self, index: int) -> float | int | str:
        """
        Returns median of the column if it's numeric.
        """
    def get_median_ad(self, index: int) -> float | int | str:
        """
        Returns meadian absolute deviation of the column if it's numeric.
        """
    def get_min(self, index: int) -> float | int | str:
        """
        Returns minimum value of the column.
        """
    def get_null_columns(self) -> list[int]:
        """
        Get indices of columns with only null values.
        """
    def get_num_nulls(self, index: int) -> float | int | str:
        """
        Returns number of nulls in the column.
        """
    def get_number_of_columns(self) -> int:
        """
        Get number of columns in the table.
        """
    def get_number_of_distinct(self, index: int) -> int:
        """
        Get number of unique values in the column.
        """
    def get_number_of_negatives(self, index: int) -> float | int | str:
        """
        Returns number of negative numbers in the column if it's numeric.
        """
    def get_number_of_values(self, index: int) -> int:
        """
        Get number of values in the column.
        """
    def get_number_of_zeros(self, index: int) -> float | int | str:
        """
        Returns number of zeros in the column if it's numeric.
        """
    def get_quantile(
        self, part: float, index: int, calc_all: bool = False
    ) -> float | int | str:
        """
        Returns quantile of the column if its type is comparable.
        """
    def get_skewness(self, index: int) -> float | int | str:
        """
        Returns skewness of the column if it's numeric.
        """
    def get_sum(self, index: int) -> float | int | str:
        """
        Returns sum of the column's values if it's numeric.
        """
    def get_sum_of_squares(self, index: int) -> float | int | str:
        """
        Returns sum of numbers' squares in the column if it's numeric.
        """
    def is_categorical(self, index: int, quantity: int) -> bool:
        """
        Check if quantity is greater than number of unique values in the column.
        """
    def show_sample(
        self,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        str_len: int = 10,
        unsigned_len: int = 5,
        double_len: int = 10,
    ) -> list[list[str]]:
        """
        Returns a table slice containing values from rows in the range [start_row, end_row] and columns in the range [start_col, end_col]. Data values are converted to strings.
        """

Default = DataStats
