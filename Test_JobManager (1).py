import pytest
import shutil
import os
from job import Job
from JobManager import JobManager


@pytest.fixture(autouse=True)
def restore_sample_data():
    """Backup and restore sample_data.csv after each test"""
    # Backup the original file before test
    if os.path.exists("sample_data.csv"):
        shutil.copy("sample_data.csv", "sample_data_backup.csv")

    yield  # Run the test

    # Restore the original file after test
    if os.path.exists("sample_data_backup.csv"):
        shutil.copy("sample_data_backup.csv", "sample_data.csv")
        os.remove("sample_data_backup.csv")

def test_JobManager_empty():
    manager = JobManager()
    assert manager.get_jobs() == []

def test_JobManager_with_jobs():
    j1 = Job("Alice", "Cleaning", 15, "12/11/2025", 4)
    j2 = Job("Bob", "Washing", 12, "13/11/2025", 3)
    jm = JobManager([j1, j2])
    jobs_list = jm.get_jobs()
    assert len(jobs_list) == 2
    assert j1 in jobs_list
    assert j2 in jobs_list

def test_JobManager_str_repr():
    manager = JobManager()
    job = Job("Bob", "Washing", 12, "13/11/2025", 3)
    manager.add_job(job)
    #expected result
    expected_str = 'JobManager: Jobs [Job("Bob", "Washing", 12, "13/11/2025", 3)]'
    #test if str and repr are the same as expected
    assert str(manager) == expected_str
    assert repr(manager) == expected_str



def test_add_jobs():
    jm = JobManager()

    #add a job below 8 hours
    job1 = Job("Alice", "Cleaning", 15, "13/11/2025", 4)
    jm.add_job(job1)
    assert jm.get_jobs() == [job1]

    #add another job for the same person that reaches exactly 8 hours
    job2 = Job("Alice", "washing", 12, "13/11/2025", 4) #4+4=8
    jm.add_job(job2)
    assert jm.get_jobs() == [job1, job2]

    #try to add another job, that will exceed 8 hours, hence it should fail
    job3 = Job("Alice", "restocking", 12, "13/11/2025", 2) #4+4+2=10
    with pytest.raises(ValueError):
        jm.add_job(job3)

def test_remove_jobs():
    jm = JobManager()
    job1 = Job("Alice", "Cleaning", 15, "13/11/2025", 4)

    #add job to jm
    jm.add_job(job1)

    #remove job from jm
    jm.remove_job(job1)
    assert jm.get_jobs() == []

def test_edit_jobs():
    jm = JobManager()
    #add old job
    old_job = Job("Alice", "Cleaning", 15, "13/11/2025", 4)
    jm.add_job(old_job)

    #replace it with new_job
    new_job = Job("Alice", "restocking", 14.65, "13/11/2025", 3)
    jm.edit_job(old_job, new_job)

    #check that the job list now contains only the new job
    assert jm.get_jobs() == [new_job]


def test_search_by_category():
    #create a JobManager instance
    jm = JobManager()
    job = Job("Alice", "Cleaning", 15, "13/11/2025", 4)
    # add the job to JobManager
    jm.add_job(job)
    #test that by searching the existing category it returns the same job
    assert jm.search_by_category("Cleaning") == [job]
    #test that by searching a diff category it returns an empty list
    assert jm.search_by_category("Washing") == []

def test_search_by_rate():
    #create a JobManager Instance
    jm = JobManager()
    #Add job to JobManager
    job = Job("Alice", "Cleaning", 15, "13/11/2025", 4)
    jm.add_job(job)
    #test that by searching the existing rate it returns the same job
    assert jm.search_by_rate(15) == [job]
    #test that by searching for a diff category it returns am empty list
    assert jm.search_by_rate(12) == []

def test_search_by_name_and_date():
    jm = JobManager()
    job = Job("Alice", "Cleaning", 15, "13/11/2025", 4)
    jm.add_job(job)
    # test that by searching the existing name and date it returns the same job
    assert jm.search_by_name_and_date("Alice","13/11/2025") == [job]
    # test that by searching for a diff name or date it returns am empty list
    assert jm.search_by_name_and_date("Candice","13/11/2025") == []

def test_get_total_cost_per_name():
    #create JobManager instance
    jm = JobManager()

    #create two jobs
    job1 = Job("Alice", "Cleaning", 15, "13/11/2025", 4)
    job2 = Job("Alice", "Washing", 12, "13/11/2025", 3)

    #add jobs to JobManager
    jm.add_job(job1)
    jm.add_job(job2)

    # expected total cost = (12*3) + (15*4) = 96
    # check if expected total cost = result
    assert jm.get_total_cost_per_name(["Alice"]) == {"Alice": 96}

def test_category_count_per_name():
    jm = JobManager()

    #create three jobs
    job1 = Job("Alice", "Cleaning", 15, "13/11/2025", 4)
    job2 = Job("Alice", "Washing", 12, "13/11/2025", 3)
    job3 = Job("Alice", "Cleaning", 15, "18/11/2025", 2)

    #add all three jobs to JobManager
    jm.add_job(job1)
    jm.add_job(job2)
    jm.add_job(job3)

    #expected Result
    expected = {"Alice":{"Cleaning": 2, "Washing":1}}

    #check if the result is the same as the expected result
    assert jm.get_category_count_per_name() == expected

def test_load_from_file():
    jm = JobManager()
    jm.load_from_file("sample_data.csv")

    # Assert
    assert len(jm.jobs) > 0  # checks that something loaded
    assert len(jm.jobs) == 24

def test_save_to_file():
    # create a new jobmanager and add some jobs
    jm = JobManager()
    jm.jobs.append(Job("Alice", "Cleaning", 15, "13/11/2025", 4))

    jm.save_to_file("sample_data.csv")
    assert os.path.exists("sample_data.csv")

    # Read the file to check the last two lines match our test jobs
    with open("sample_data.csv", 'r') as f:
        lines = f.readlines()

    # Check header is correct
    assert lines[0].strip() == "name,category,hours,rate,date"

    # Check the last two lines contain the jobs we added
    assert lines[-1].strip() == "Alice,Cleaning,4,15,13/11/2025"
















