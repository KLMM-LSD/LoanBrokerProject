python ../../Svedbanken/svedbanken.py &
SVED=$!
python ../../Normalizer/normalizer.py &
NORM=$!
python ../../Aggregator/aggregator.py &
AGGR=$!

