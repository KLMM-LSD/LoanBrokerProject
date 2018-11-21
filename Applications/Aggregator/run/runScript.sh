python3 ../../Svedbanken/svedbanken.py &
SVED=$!
python3 ../../Normalizer/normalizer.py &
NORM=$!
python3 ../../Aggregator/aggregator.py &
AGGR=$!

