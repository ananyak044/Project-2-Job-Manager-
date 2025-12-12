#parent class
import os
from job import Job
class JobManager:

    #constructor
    def __init__(self, jobs=None):
        if jobs is None:
            self.jobs = []
        else:
            self.jobs = jobs

    def get_jobs(self):
        return self.jobs

    def __str__(self):
        return f'JobManager: Jobs {self.jobs}'

    def __repr__(self):
        return self.__str__()

    def add_job(self, job):
        #check total hours of the worker
        total_hours = 0
        for j in self.jobs:
            if j.name == job.name and j.date == job.date:
                total_hours += j.hours

        #check if it exceeds the limit
        if total_hours + job.hours > 8:
            raise ValueError(f'Job {job.name} has more than 8 hours')
        else:
            self.jobs.append(job)

    def remove_job(self, job):
        self.jobs.remove(job)

    def edit_job(self, old_job, new_job):
        self.jobs.remove(old_job)
        #check availability for the new job
        total_hours = 0
        for j in self.jobs:
            if j.name == new_job.name and j.date == new_job.date:
                total_hours += j.hours

        # check if it exceeds the limit
        if total_hours + new_job.hours > 8:
            raise ValueError(f'Job {new_job.name} has more than 8 hours')
        else:
            self.jobs.append(new_job)

    def search_by_category(self, category):
        matching_categories = []
        for j in self.jobs:
            if j.category == category:
                matching_categories.append(j)
        return matching_categories

    def search_by_rate(self, rate):
        matching_rates = []
        for j in self.jobs:
            if j.rate == rate:
                matching_rates.append(j)
        return matching_rates

    def search_by_name_and_date(self, name, date):
        matching_jobs = []
        for j in self.jobs:
            if j.name == name and j.date == date:
                matching_jobs.append(j)
        return matching_jobs

    def get_total_cost_per_name(self, names):
        total_cost = {}
        for name in names:
            # sum all jobs for this worker
            cost = sum(j.rate * j.hours for j in self.jobs if j.name == name)
            total_cost[name] = cost
        return total_cost

    def get_category_count_per_name(self):
        result = {}
        for j in self.jobs:
            if j.name not in result:
                result[j.name] = {}
            if j.category not in result[j.name]:
                result[j.name][j.category] = 0
            result[j.name][j.category] += 1
        return result

    def load_from_file(self, file_name):
        import csv
        self.jobs = []
        with open(file_name, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['name']:  # skip empty rows
                    continue
                name = row['name']
                category = row['category']
                hours = int(float(row['hours']))  # ensure hours is int
                rate = float(row['rate'])
                date = row['date']
                self.jobs.append(Job(name, category, rate, date, hours))

    def save_to_file(self, file_name):
        import csv
        file_exists = os.path.exists(file_name)
        with open(file_name, 'a', newline='') as f:
            fieldnames = ['name', 'category', 'hours', 'rate', 'date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for j in self.jobs:
                writer.writerow({
                    'name': j.name,
                    'category': j.category,
                    'hours': j.hours,
                    'rate': j.rate,
                    'date': j.date
                })





