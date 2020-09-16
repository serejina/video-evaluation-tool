"""
Module contains functions to calculate PSNR for video files
"""
import cv2 as cv
import numpy as np
import logging

from .exceptions import VideoCaptureException


def prepare_inputs_video(source_ref, source_comp):
    """
    Opens and checks inputs video files for video capturing.
    :param source_ref: name of reference video file
    :param source_comp: name of video file to compare
    :return: the opened reference video file and the opened compared video file (openCV VideoCapture objects)
    :raise VideoCaptureException if input files can not be opened or have different dimensions
    """
    ref_rnc = cv.VideoCapture(source_ref)
    und_tst = cv.VideoCapture(source_comp)

    if not ref_rnc.isOpened():
        raise VideoCaptureException("Could not open {}".format(source_ref))
    if not und_tst.isOpened():
        raise VideoCaptureException("Could not open {}".format(source_comp))

    ref_size = (int(ref_rnc.get(cv.CAP_PROP_FRAME_WIDTH)), int(ref_rnc.get(cv.CAP_PROP_FRAME_HEIGHT)))
    und_tst_size = (int(und_tst.get(cv.CAP_PROP_FRAME_WIDTH)), int(und_tst.get(cv.CAP_PROP_FRAME_HEIGHT)))

    if ref_size != und_tst_size:
        raise VideoCaptureException(
            "Different size of videos\n{}: width {} height {}\n{}: width {} height {}".format(
                source_ref, ref_size[0], ref_size[1], source_comp, und_tst_size[0], und_tst_size[1]))
    return ref_rnc, und_tst


def get_psnr_frame(org_matrix, comp_matrix):
    """
    Calculates PSNR according to the formula https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    :param org_matrix: the matrix data of original image
    :param comp_matrix: the matrix data of the compared image
    :return: PSNR value, 0 if PSNR value too small (<= 1E^-10)
    """
    MAX = 255
    s1 = cv.absdiff(org_matrix, comp_matrix)
    s1 = np.float32(s1)
    s1 = s1 * s1
    sse = s1.sum()
    if sse <= 1e-10:
        return 0
    else:
        shape = org_matrix.shape
        mse = (1.0 * sse) / (shape[0] * shape[1] * shape[2])
        psnr = 10 * np.log10((MAX * MAX) / mse)
        return psnr


def _frame_none_check(frame_id, frame, num_frames, file_name):
    """
    Checks that a frame is None, log warning if the frame is not last
    :param frame_id: sequence number of the frame
    :param frame: the frame to check
    :param num_frames: numbers of all frames
    :param file_name: video file name
    :return: True when the frame is None
    """
    if frame is None:
        if frame_id < num_frames:
            logging.warning("{} frame #{} is None. PSNR were calculated till this frame".format(file_name, frame_id))
        return True


def processing_psnr(source_ref, source_comp):
    """
    Performs PSNR calculation between two two video files
    :param source_ref: the path to reference input video file
    :param source_comp: the path to the video file for comparison with source_ref
    :return: general_info, psnr_result: list with psnr for each frame and the general information about how many frames in total for source_ref
                                        and source_comp, i.e. psnr_result - [(frame_id_0, psnr_0), (frame_id_1, psnr_1)...]
                                        general_info - {"general": {"source_ref": <whole number of frames in source_ref>,
                                                                    "source_comp": <whole number of frames in source_comp>
                                                                   } }
    """
    psnr_result = []
    cap_ref_rnc, cap_und_tst = prepare_inputs_video(source_ref, source_comp)
    cap_ref_frames = int(cap_ref_rnc.get(cv.CAP_PROP_FRAME_COUNT))
    cap_und_tst_frames = int(cap_und_tst.get(cv.CAP_PROP_FRAME_COUNT))
    general_info = {"general": {source_ref: cap_ref_frames, source_comp: cap_und_tst_frames}}
    frame_id = 0
    while True:
        _, frame_ref = cap_ref_rnc.read()
        _, frame_und_tst = cap_und_tst.read()
        if _frame_none_check(frame_id, frame_ref, cap_ref_frames, source_ref) or _frame_none_check(frame_id,
                                                                                                   frame_und_tst,
                                                                                                   cap_und_tst_frames,
                                                                                                   cap_und_tst_frames):
            break
        psnr = get_psnr_frame(frame_ref, frame_und_tst)
        res_info = (frame_id, round(psnr, 3))
        psnr_result.append(res_info)
        frame_id += 1
    return general_info, psnr_result
