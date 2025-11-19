# tests/test_train.py
import glob

def test_csv_exists():
    files = glob.glob("data/*UNSW*.csv") + glob.glob("data/*.csv")
    assert len(files) > 0, "No CSV found under data/ — set DATA_URL secret to a direct link"
