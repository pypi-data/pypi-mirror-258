'''
Calculate precision, recall, precisionrecallfscore,
coverage, purity, and coveragepurityfscore using Pyannote
Drop missing values before calculating the evaluation metric
'''

import os
import pandas as pd
from numpy import NaN

from pyannote.core import Annotation, Timeline, Segment
from pyannote.metrics.segmentation import SegmentationPrecision, SegmentationRecall, \
    SegmentationCoverage, SegmentationPurity


def calculate_detection_metrics(prediction_output_path, labelled_data_path, csv_filename, tolerance=0.5):
    '''
    The function calculates metrics to evaluate the performance of speaker change detection models. The calculated metrics
    are segment precision, segment recall, segment precision recall f1 score,
    segment coverage, segment purity, and segment purity f1 score.

    The function uses the csv files of speaker change detection predictions and true labels to calculate the metrics.
    The speaker change detection predictions csv file should contain start, end, and speaker_change column to indicate
    if speaker change is True or False from the start to the end of every segment.

    The speaker change detection labels csv file should contain bgn, duration, and speaker column (corresponding to the
    standardized rttm format) to indicate each speaker from the bgn of every segment with the duration.

    :param prediction_output_path: A path where the csv file of speaker change detection predictions is saved
    :type prediction_output_path: str
    :param labelled_data_path: A path where the csv file of speaker change detection true labels is saved
    :type labelled_data_path: str
    :param csv_filename: A name of the csv files of speaker change detection predictions and true labels
    :type csv_filename: str
    :param tolerance: The maximum distance between two boundaries of time segments for them to be matched.
    :type tolerance: float
    :return: None
    :rtype: None
    '''
    # Read Prediction and Labelled DF
    prediction_df = pd.read_csv(os.path.join(prediction_output_path, csv_filename))
    labelled_df = pd.read_csv(os.path.join(labelled_data_path, csv_filename))

    # Parse Inputs to Data Structures in Metrics Module
    labelled_df['end'] = labelled_df['bgn'] + labelled_df['duration']
    labels_segments = Timeline()
    labels_annotation = Annotation()
    for idx, row in labelled_df[['bgn', 'end', 'speaker']].iterrows():
        time_segment = Segment(row['bgn'], row['end'])
        labels_segments.add(time_segment)
        labels_annotation[time_segment] = row['speaker']

    # Initialize Metrics Class
    coverage_score = SegmentationCoverage(tolerance=tolerance)
    purity_score = SegmentationPurity(tolerance=tolerance)
    precision_score = SegmentationPrecision(tolerance=tolerance)
    recall_score = SegmentationRecall(tolerance=tolerance)

    # Initialize Evaluation DataFrame
    evaluation_df = pd.DataFrame()
    # List Six Metrics for Calculation
    metrics_names_list = ['precision', 'recall', 'precision_recall_f1', 'coverage', 'purity', 'coverage_purity_f1']
    evaluation_df['metric_name'] = metrics_names_list
    evaluation_df['audio_file_name'] = [csv_filename.split('.')[0]] * len(metrics_names_list)

    # Check imbalance dataset; Baseline: If predict all speaker change as true or false
    num_speaker_changes = 0
    prev_speaker = labelled_df.iloc[0]['speaker']
    for speaker in labelled_df.iloc[1:]['speaker']:
        if speaker != prev_speaker:
            num_speaker_changes += 1
            prev_speaker = speaker
    proportion_no_speaker_changes = 1 - num_speaker_changes/labelled_df.shape[0]
    evaluation_df['proportion_no_speaker_changes'] = proportion_no_speaker_changes

    # Calculate Evaluation Metrics for All Models
    speaker_change_models_cols = [col for col in prediction_df.columns if 'speaker_change' in col and 'true' not in col]
    for speaker_change_col in speaker_change_models_cols:
        # Parse Inputs into Data Structures on Metrics Module
        prediction_segments = Timeline()
        start_segment = prediction_df.iloc[0]['start']
        end_segment = prediction_df.iloc[0]['end']

        # Append pseudo last row with speaker change col TRUE to deal with the last row exception
        # If the real last row is FALSE, then merge all false speaker segments including the real last row together
        # If the real last row is TRUE, then the real last row itself is also the independent segment
        prediction_df.loc[len(prediction_df)] = prediction_df.iloc[-1]
        # New row is appended
        prediction_df.loc[len(prediction_df)-1, speaker_change_col] = True

        for current_row_idx, row in prediction_df.iterrows():
            if current_row_idx == 0:  # No speaker changes information of the first row
                continue
            # If speaker_change = True, merge previous false speaker change segments together
            if row[speaker_change_col]:
                prediction_segments.add(Segment(start_segment, end_segment))
                start_segment = row['start']
                end_segment = row['end']
            else:
                end_segment = row['end']
        precision = precision_score(labels_segments, prediction_segments)
        recall = recall_score(labels_segments, prediction_segments)
        if (precision+recall != 0):
            precision_recall_f1 = 2 * precision * recall / (precision + recall)
        else:
            precision_recall_f1 = NaN
        coverage = coverage_score(labels_annotation, prediction_segments)
        purity = purity_score(labels_annotation, prediction_segments)
        if (coverage+purity != 0):
            coverage_purity_f1 = 2 * coverage * purity / (coverage + purity)
        else:
            coverage_purity_f1 = NaN
        evaluation_df[speaker_change_col] = [precision, recall, precision_recall_f1, coverage, purity,
                                             coverage_purity_f1]
    return evaluation_df


