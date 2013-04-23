for n in examples.py/*; do
	PYTHONPATH=. python2 "$n" > examples.pb/`basename "$n" .py`.pb
done

