Fake Stock Data
===============

This downloads daily quotes for the S&P 500 from
[www.quantquote.com](https://quantquote.com/historical-stock-data)'s historical
averages and then "fills in" more frequent data using random numbers while
still respecting open/close/low/high of the daily trends.

This is useful in teaching and testing scenarios when you want to have an
arbitrarily large volume of realistic looking tabular data without downloading
or procuring actual datasets.  Long-scale correlations and trends should be
accurate while short-term correlations and trends are non-sense.

TO BE PERFECTLY CLEAR.  THE DATA COMING FROM THIS PROJECT IS NOT ACCURATE.  IT
SHOULD ONLY BE USED FOR COMPUTATIONAL TESTING OR EDUCATION.

For convenience some daily quote data is shipped in this repository.  This data
is thanks to the free data generously provided by www.quantquote.com .

Use
---

    $ ipython

    >>> from fakestockdata import generate_stocks
    >>> generate_stocks(freq=pd.Timestamp(minutes=1))
