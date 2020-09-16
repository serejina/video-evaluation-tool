"""
Module to represent metrics for video analysis
"""
import numpy as np


class Metrics(object):

    def __init__(self, psnrs_info):
        """
        Parameterized constructor with psnrs_info parameter to instantiate class instance
        :param psnrs_info:  List with psnr values. Each element of the list shall be represented as (frame_id, psnr_val)
        """
        self._psnrs_numbers = [psnr[1] for psnr in psnrs_info]
        self.psnr_array = np.array(self._psnrs_numbers)

    @property
    def min_psnr(self) -> float:
        """
        :return:    Minimum value from provided psnr list
        """
        return np.amin(self.psnr_array)

    @property
    def max_psnr(self) -> float:
        """
        :return: Maximum value from provided psnr list
        """
        return np.amax(self.psnr_array)

    @property
    def median_psnr(self) -> float:
        """
        :return: Median value from provided psnr list
        """
        return np.median(self.psnr_array)

    def get_filtered_psnr(self, function, parameter):
        """
        Returns filtered psnr values, size of the filtered values and ratio of filtered to all in %
        :param function:    function to use for the psnr value comparison,
                            the function shall take two arguments (all prns values,  parameter),
                            i.e. lambda psnr, threshold: psnr > threshold
        :param parameter:   parameter to use in the comparison function
        :return:            size of the filtered values, the ratio rounded by 3 and filtered psnr values
        """
        filtered_data = self.psnr_array[function(self.psnr_array, parameter)]
        filtered_full_ration = (filtered_data.size / self.psnr_array.size) * 100
        return filtered_data.size, round(filtered_full_ration, 3), filtered_data
