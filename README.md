# D-fine

A webapp to define words and phrases

## How to use

* Install [Redis](http://redis.io/)
* Setup virtualenv
<pre>
    virtualenv --no-site-packages ./
    . bin/active
    pip install -r requirements.txt
</pre>

* Run the Webapp
<pre>
    python webserver.py
</pre>


Note: D-fine *will* work without redis, but all the data be lost on each restart.



## Why I build this

Two reasons:

1. To scratch an itch I had for an easy to use definition site.
1. To play around more with Flask and virtualenv.


### TODO

* Switch back to using cdnjs.com for the javascript files
* Fix the date/time
* Maybe add a fall back to a standard dictionary site
