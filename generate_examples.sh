for n in examples.py/*; do
	echo Processing "$n"
	echo "  =>" examples.pb/`basename "$n" .py`.pb
	PYTHONPATH=. python2 "$n" > examples.pb/`basename "$n" .py`.pb
done

