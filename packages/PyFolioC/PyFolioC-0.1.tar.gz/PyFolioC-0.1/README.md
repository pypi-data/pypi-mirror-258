# PyFolioC


The PyFolioCC class is designed to build an optimal portfolio in the sense of Markowitz using general graph clustering 
techniques. The idea is to provide a historical return database of an asset universe (historical_data), a lookback window 
(lookback_window) for portfolio construction, a number of clusters (number_clusters), a clustering method (clustering_method), 
and an evaluation window (evaluation_window). From there, the objective is to construct a portfolio based on historical return 
data over the period corresponding to lookback_window by creating a sub-portfolio composed of a specified number of synthetic 
assets (ETFs) using the clustering method specified in clustering_method. The performance (Sharpe ratio and cumulative PnL) of
the constructed portfolio is then evaluated over the evaluation_window.

