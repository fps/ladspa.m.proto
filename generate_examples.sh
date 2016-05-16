install -d examples.pb
set -e
for n in examples.py/*.py; do
	echo Processing "$n"
	echo "  =>" examples.pb/`basename "$n" .py`.pb
	PYTHONPATH=. python2 "$n" > examples.pb/`basename "$n" .py`.pb
done

