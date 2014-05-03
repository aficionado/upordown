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

from bigmler.utils import log_message, dated, is_shared
from bigml.api import get_resource_type


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


def get_updater(api, resource_type):
    """Returns the method to update a given resource type

    """
    updaters = {
        "source": api.update_source,
        "dataset": api.update_dataset,
        "model": api.update_model,
        "ensemble": api.update_ensemble,
        "batchprediction": api.update_batch_prediction,
        "prediction": api.update_prediction,
        "evaluation": api.update_evaluation
    }
    return updaters[resource_type]


def share_resource(api, resource):
    """Creates a secret link to share the resource.

    """
    resource_type = get_resource_type(resource)
    resource = get_updater(api, resource_type)(resource, {"shared": True})
    if api.ok(resource) and is_shared(resource):
        return ("https://bigml.com/shared/%s/%s" %
                (resource_type, resource['object']['shared_hash']))
    else:
        sys.exit("Failed to share the resource: %s" % resource['resource'])
