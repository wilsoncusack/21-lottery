# 21-lottery

* Project up at: http://two1-lottery.herokuapp.com/

* To get just the client file and hit the endpoint, run:
```
wget https://raw.githubusercontent.com/wilsoncusack/21-lottery/master/play.py -O <target file path>
```
then
```
python3 <targeted_file.py>
```

### How it works:
* In each round, a random winning bet number is picked between 1 and n, where n is the round size (the round size is twice the size of the last, starting at 10. Ex: 10, 20, 40, 80, etc...)
* Each hit to the endpoint cost 1000 Satoshi, that money is added to each round's winning pot
* The winning better received 50% of the total pot, the remaining 50% is rolled-over into the next round's pot

#### Example:
Round 1 size: 10
Starting pot size: 0
Winning bet #: 6
Better #6 receives 6,000 Satoshi back (including their 1000 bet being returned)
----
Round 2 size: 20
Starting pot size: 5000
Winning bet #: 18
Better #18 receives 24,000 Satoshi (including their 1000 bet being returned)
