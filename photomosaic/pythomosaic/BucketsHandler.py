from .constants import DIST_MAX_COLOR_BUCKET
from .utils import euclidean_distance
from .Bucket import Bucket
from .Element import Element


class BucketsHandler:
    def __init__(self, buckets: list[Bucket] = None) -> None:
        self.buckets = buckets if buckets is not None else []

    def empty_buckets(self) -> None:
        self.buckets = []

    def elements_to_buckets(self, elements: list[Element]) -> None:
        """
        Sort the elements into buckets
        :param elements: the list of elements
        """
        for element in elements:
            # if the element is black only skip it
            if element.color[0] == 0 and element.color[1] == 0 and element.color[2] == 0:
                continue

            # if there are no buckets create one and add the element
            if len(self.buckets) == 0:
                bucket = Bucket([element])
                self.buckets.append(bucket)
                continue

            # if there are buckets find the closest one
            min_dist = 10000
            bucket_target = None

            for bucket in self.buckets:
                dist = euclidean_distance(
                    bucket.average_color,
                    element.color
                )
                if dist < min_dist:
                    bucket_target = bucket
                    min_dist = dist

            # check if the closest bucket is close enough to add the element else create a new bucket
            if min_dist < DIST_MAX_COLOR_BUCKET:
                bucket_target.add_element(element)
            else:
                bucket = Bucket([element])
                self.buckets.append(bucket)
