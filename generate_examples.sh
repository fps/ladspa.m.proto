for n in examples.py/*; do
	PYTHONPATH=. python2 "$n" > examples.pb/`basename -s .py "$n"`.pb
done

