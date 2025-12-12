import pytest
from job import Job

def test_job_creation():
    j = Job("Alice","cleaning", 15, "12/11/2025", 4)
    assert j.name == "Alice"
    assert j.category == "cleaning"
    assert j.rate == 15
    assert j.date == "12/11/2025"
    assert j.hours == 4

def test_invalid_rate():
    with pytest.raises(ValueError):
        Job("Alice","cleaning", -15, "12/11/2025", 4)

def test_invalid_hours():
    # hours<0
    with pytest.raises(ValueError):
        Job("Alice","cleaning", 15, "12/11/2025", -4)

    # hours>6
    with pytest.raises(ValueError):
        Job("Alice","cleaning", 15, "12/11/2025", 8)

def test_getters():
    j = Job("bob","washing", 13.45, "16/12/2025", 5)
    assert j.get_name() == "bob"
    assert j.get_category() == "washing"
    assert j.get_rate() == 13.45
    assert j.get_date() == "16/12/2025"
    assert j.get_hours() == 5

def test_job_str_repr():
    j = Job("candice","washing", 12.35, "21/11/2025", 2)
    expected_str = 'Job("candice", "washing", 12.35, "21/11/2025", 2)'
    #test __str__
    assert str(j) == expected_str
    #test __repr__
    assert repr(j) == expected_str

def test_job_eq():
    j = Job("candice", "washing", 12.35, "21/11/2025", 2)
    other = Job("candice", "washing", 12.35, "21/11/2025", 2)
    assert j == other

def test_job_hash():
    job1 = Job("John", "cleaning", 16, "22/11/2025", 4)
    job2 = Job("John", "cleaning", 16, "22/11/2025", 4)
    job3 = Job("John", "washing", 12.35, "21/11/2025", 2)
    #same objects should have the same hash
    assert hash(job1) == hash(job2)
    #different objects should ideally have different hash
    assert hash(job1) != hash(job3)
