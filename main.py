"""Module contains main function
"""
from source.config import Config
from source.metrics import Metrics
from source.psnr import processing_psnr
from source.exceptions import VideoCaptureException
from source.report import create_report
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def main():
    """
        The function performs coding evaluation according to the following steps:
        1. Instantiate config object and initialize parameters to report, define path to the report file
        2. Iterate through all videos in the config, for each one:
            2.1 Calculate PSNR
            2.2 Calculate metrics (min, max, median, ratio)
            2.3 create record for the report with calculated data
            2.4 update list with metrics
        3. Update report data with metric list for each video
        4. Create report with report data
    :return:
    """
    # configuration file with input information
    cfg = Config("config/input_config_1.json")

    # parameters for report
    report_path = os.path.join(cfg.report_folder, "report_{}.html".format(datetime.now().strftime("%Y%m%d_%H_%M_%3S")))
    reports_data = {"total_videos": len(cfg.videos)}
    metrics_list = []

    # run video analysis
    for idx, input_videos in enumerate(cfg.videos):
        logging.info("videos: {} {}".format(input_videos.reference_video, input_videos.compressed_video))
        try:
            # calculate psnr values
            gen_info, psnrs_info = processing_psnr(input_videos.reference_video, input_videos.compressed_video)

            # analysis
            metrics = Metrics(psnrs_info)
            # min, max, median
            min, max, median = metrics.min_psnr, metrics.max_psnr, metrics.median_psnr
            # get ratio for all threshold values from the config file
            ratio = metrics.get_filtered_psnr(lambda psnr, threshold: psnr < threshold, input_videos.threshold)[1]

            # prepare record to report
            report_rec = {idx: {"original": input_videos.reference_video,
                                "compressed": input_videos.compressed_video,
                                "Number of frames reference": gen_info["general"][input_videos.reference_video],
                                "Number of frames compressed": gen_info["general"][input_videos.compressed_video],
                                "Number of processed frames": len(psnrs_info),
                                "max PSNR, dB": max,
                                "min PSNR, dB": min,
                                "median PSNR, dB": median,
                                "Ratio of PSNR being below {} dB, %".format(input_videos.threshold): ratio,
                                "PSNR": psnrs_info}}
            metrics_list.append(report_rec)
        except VideoCaptureException:
            logging.warning("videos: {} and {} were skipped since VideoCaptureException happened".format(
                input_videos.reference_video, input_videos.compressed_video))
            continue

    # create report
    reports_data.update({"metrics": metrics_list})
    create_report(report_name=report_path, report_data=reports_data)


if __name__ == "__main__":
    main()
