Up or Down?
===========

Predicting whether a stock will go up or down using BigML and data from Quandl
and PsychSignal

Predicting whether a stock will go up or down using data from [Quandl](http://www.quandl.com/) and ([PsychSignal](https://psychsignal.com/).

## Analyzing the data

1. Install bigmler:

        pip install bigmler

2. Set up your BIGML_USERNAME and BIGML_API_KEY

        [Setting up BigML authentication](https://bigml.com/developers/quick_start#q_authenticate)

3. Run the script

        ./upordown.py
        [2014-05-01 22:17:05] Creating sources...
        [2014-05-01 22:17:20] Creating datasets...
        [2014-05-01 22:17:39] Merging datasets...
        [2014-05-01 22:18:03] Splitting dataset...
        [2014-05-01 22:18:07] Creating a model using the training dataset...
        [2014-05-01 22:18:10] Evaluating model against the test dataset...
        [2014-05-01 22:18:13] Creating an ensemble using the training dataset...
        [2014-05-01 22:18:30] Evaluating ensemble against the test dataset...
        [2014-05-01 22:18:35] Creating model for the full dataset...
        [2014-05-01 22:18:37] Sharing resources...
        [2014-05-01 22:18:40] https://bigml.com/shared/dataset/zy156fHO5woBGSbTuNeJbkg3htM
        [2014-05-01 22:18:40] https://bigml.com/shared/model/jQNDNqxcSDsfKmQp10cIEXV2Jb7
        [2014-05-01 22:18:40] https://bigml.com/shared/evaluation/oQttuHuCiJ0DW01ai1OsVrsGvww
        [2014-05-01 22:18:40] https://bigml.com/shared/evaluation/3w8Baa5yb5sHliJzHMSZJ2PplW8

## Visualizing the data

* [Dataset](https://bigml.com/shared/dataset/zy156fHO5woBGSbTuNeJbkg3htM)

<img src="https://raw.github.com/aficionado/upordown/master/images/dataset.png" alt="Dataset">

* [Model](https://bigml.com/shared/model/jQNDNqxcSDsfKmQp10cIEXV2Jb7)

<img src="https://raw.github.com/aficionado/upordown/master/images/sunburst.png" alt="Sunburst">

* [Single model evaluation](https://bigml.com/shared/evaluation/oQttuHuCiJ0DW01ai1OsVrsGvww)

<img src="https://raw.github.com/aficionado/upordown/master/images/confusion_matrix_model.png" alt="Single model evaluation">

* [Ensemble evaluation](https://bigml.com/shared/evaluation/3w8Baa5yb5sHliJzHMSZJ2PplW8)

<img src="https://raw.github.com/aficionado/upordown/master/images/confusion_matrix_ensemble.png" alt="Ensemble evaluation">
