#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) 2014 BigML, Inc
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##############################################################################
"""Playing with Quandl and Psychsignal data.

"""
import os
import sys
import argparse
import glob

from bigml.api import BigML

from utils import log, training_test_split, previous
from utils import share_resource


def daily_change():
    """Price at closing minus price at opening.

    """
    return ["-", ["f", "Close"], ["f", "Open"]]


def normalize_previous_close():
    """Price at closing of the previous day minus the price at opening
    of the previous day over the price at opening of the previous day.

    """
    return ["/", ["-", previous("Close"),
            previous("Open")], previous("Open")]


def normalize_open():
    """Price at closing of the previous day minus the price at opening
    over the price at closing of the previous day.

    """
    return ["/", ["-", previous("Close"), ["f", "Open"]], previous("Close")]


def new_fields():
    """Generates JSON s-expression for new fields.

    """
    return [
        {"name": "Close-1",
         "field": normalize_previous_close()},
        {"name": "Open",
         "field": normalize_open()},
        {"name": "Volume-1",
         "field": previous("Volume")},
        {"name": "Bullish-1",
         "field": previous("Bullish")},
        {"name": "Bearish-1",
         "field": previous("Bearish")},
        {"name": "UpOrDown?",
         "field": ["if", [">", daily_change(), 0], "Up", "Down"]}]


def main(args=sys.argv[1:]):
    """Parses command-line parameters and calls the actual main function.

    """
    parser = argparse.ArgumentParser(
        description="Market sentiment analysis",
        epilog="BigML, Inc")

    # source with activity data
    parser.add_argument('--data',
                        action='store',
                        dest='data',
                        default='data',
                        help="Full path to data with csv files")

    # create private links or not
    parser.add_argument('--share',
                        action='store_true',
                        default=True,
                        help="Share created resources or not")

    args = parser.parse_args(args)

    if not args.data:
        sys.exit("You need to provide a valid path to a data directory")

    api = BigML()

    name = "UpOrDown?"

    log("Creating sources...")
    csvs = glob.glob(os.path.join(args.data, '*.csv'))
    sources = []
    for csv in csvs:
        source = api.create_source(csv)
        api.ok(source)
        sources.append(source)

    log("Creating datasets...")
    datasets = []
    for source in sources:
        dataset = api.create_dataset(source)
        api.ok(dataset)
        datasets.append(dataset)

    new_datasets = []
    for dataset in datasets:
        new_dataset = api.create_dataset(dataset, {
            "new_fields": new_fields(),
            "all_fields": False})
        new_datasets.append(new_dataset)

    log("Merging datasets...")
    multi_dataset = api.create_dataset(new_datasets, {'name': name})
    api.ok(multi_dataset)

    # Create training and test set for evaluation
    log("Splitting dataset...")
    training, test = training_test_split(api, multi_dataset)

    log("Creating a model using the training dataset...")
    model = api.create_model(training, {'name': name + ' (80%)'})
    api.ok(model)

    # Creating an evaluation
    log("Evaluating model against the test dataset...")
    eval_args = {
        'name': name + ' - Single model: 80% vs 20%'}
    evaluation_model = api.create_evaluation(model, test, eval_args)
    api.ok(evaluation_model)

    log("Creating an ensemble using the training dataset...")
    ensemble = api.create_ensemble(training, {'name': name})
    api.ok(ensemble)

    # Creating an evaluation
    log("Evaluating ensemble against the test dataset...")
    eval_args = {'name': name + ' - Ensemble: 80% vs 20%'}
    evaluation_ensemble = api.create_evaluation(ensemble, test, eval_args)
    api.ok(evaluation_ensemble)

    log("Creating model for the full dataset...")
    model = api.create_model(multi_dataset, {'name': name})
    api.ok(model)

    # Create private links
    if args.share:
        log("Sharing resources...")
        dataset_link = share_resource(api, multi_dataset)
        model_link = share_resource(api, model)
        evaluation_model_link = share_resource(api, evaluation_model)
        evaluation_ensemble_link = share_resource(api, evaluation_ensemble)
        log(dataset_link)
        log(model_link)
        log(evaluation_model_link)
        log(evaluation_ensemble_link)

if __name__ == "__main__":
    main()
