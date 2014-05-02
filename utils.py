# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) 2014 BigML, Inc
# All rights reserved.
#
# This software is provided as template to interact with BigML's API.
#
# BigML hereby grants to iNostix, a royalty-free, non-exclusive,
# limited license to use this software to interact with BigML's API.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
# OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
##############################################################################
"""Utils to interact with BigML API.

"""

from bigmler.utils import log_message, dated


def log(message):
    """Dates and logs messsage.

    """
    log_message(dated(message.rstrip('\n') + '\n'), console=1)


def training_test_split(api, dataset, rate=0.8, seed='seed',
                        training='Training', test='Test'):
    """Generates disjoint training and test sets.

    """
    training_set = api.create_dataset(dataset, {
        'sample_rate': rate,
        'seed': seed,
        'name': training})
    test_set = api.create_dataset(dataset, {
        'sample_rate': rate,
        'seed': seed,
        'out_of_bag': True,
        'name': test})

    if api.ok(training_set) and api.ok(test_set):
        return training_set, test_set


def previous(field):
    """Generates s-expression to access a `field` previous value.

    """

    return ["f", field, -1]


def share_dataset(api, dataset):
    """Creates a secret link to share `dataset`.

    """
    dataset = api.update_dataset(dataset, {"shared": True})
    if api.ok(dataset):
        return ("https://bigml.com/shared/dataset/%s" %
                dataset['object']['shared_hash'])


def share_model(api, model):
    """Creates a secret link to share `model`.

    """
    model = api.update_model(model, {"shared": True})
    if api.ok(model):
        return ("https://bigml.com/shared/model/%s" %
                model['object']['shared_hash'])


def share_evaluation(api, evaluation):
    """Creates a secret link to share `evaluation`.

    """
    evaluation = api.update_evaluation(evaluation, {"shared": True})
    if api.ok(evaluation):
        return ("https://bigml.com/shared/evaluation/%s" %
                evaluation['object']['shared_hash'])
