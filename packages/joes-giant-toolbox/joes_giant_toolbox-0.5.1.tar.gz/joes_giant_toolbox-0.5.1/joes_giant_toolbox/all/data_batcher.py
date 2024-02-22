"""Defines class DataBatcher"""


class DataBatcher:
    """Breaks a provided iterable up into batches according to a
    provided batching pattern

    Example:
    >>> mydata = [1,2,3,4,5,6,7,8,9,10,11,12]
    >>> mybatcher = DataBatcher(mydata, batch_pattern=(1,2,4))
    >>> for batch in mybatcher:
    ...     print(batch)
    (1,)
    (2, 3)
    (4, 5, 6, 7)
    (8, 9, 10, 11, 12)
    """

    def __init__(self, data, batch_pattern: tuple[int, ...]) -> None:
        """Initial setup of DataBatcher class

        Args:
            data (Any): Any python iterable (list, tuple, set, str, dict etc.)
            batch_pattern (tuple[int, ...]): A list of integers describing sequence of batch sizes
                If `batch_pattern` is exhausted before `data`, the final batch contains everything
                remaining in `data`
        """
        self._data = iter(data)
        self._batch_size = iter(batch_pattern)

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        """Returns the next batch of data"""
        result = []
        try:
            batch_size: int = next(self._batch_size)
            for _ in range(batch_size):
                try:
                    result.append(next(self._data))
                except StopIteration:
                    break
        except StopIteration:  # nothing left in batch_pattern
            while self._data:
                try:
                    result.append(next(self._data))
                except StopIteration:
                    break
        if len(result) == 0:
            raise StopIteration
        return tuple(result)


if __name__ == "__main__":
    my_data = list(range(20))
    my_batch_pattern = (1, 2, 4, 1)
    print("my data:", my_data)
    print("my batch pattern:", my_batch_pattern)
    test_data_batcher = DataBatcher(my_data, my_batch_pattern)
    for batch in test_data_batcher:
        print(batch)
