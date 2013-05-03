if [ -d private ]; then
    cd private
    hg up
    cd ..
else
    hg clone ssh://hg@bitbucket.org/pyspeckit/pyspeckit-private private
fi
python private/boto_download.py --includestr fits
cd tests
python run_tests.py
python private/boto_upload.py --includesubstrdir tests_

