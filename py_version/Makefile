now:
	python3 minimax.py

oo:
	python3 oominimax.py

tests:
	make t1
	make t2
	make t3
	diff output.1 output.1.correct
	diff output.2 output.2.correct
	diff output.3 output.3.correct
t1:
	make dotest NUM=1

t2:
	make dotest NUM=2

t3:
	make dotest NUM=3

dotest:
	python3 oominimax.py < input.$(NUM) > output.$(NUM)
	diff output.$(NUM) output.$(NUM).correct
	cksum output.$(NUM)
	cksum output.$(NUM).correct

clean:
	-rm output.?
