# Top 3 User Actions
1. Adding pet and owner information
2. Creating tasks for pet (setting priority and duration)
3. View generated schedule

# Main Objects

### 1. Owner
#### Attributes:
- name (str)
- pets (list -> Pet)
- tasks (list -> Task) — owner-level task list; tasks reference a pet
- availability (dict) — e.g. {"Monday": (11, 4), ..., "Sunday": (1, 3)}
    
#### Methods:
- add_pet(name, age, species, breed=None) → creates a Pet object and appends it to pets
- add_task(task) → appends a Task object to tasks
- remove_task(task) → removes a task from the owner's task list
- get_tasks_for_pet(pet) → returns filtered list of tasks referencing a specific pet
- update_availability(day, start_time, duration) → updates a single day's availability window


### 2. Pet
#### Attributes:
- name (str)
- age (int or float) — in years
- species (str) — e.g. "dog", "cat"
- breed (str, optional)
- medical_notes (str, optional) — e.g. allergies, conditions relevant to task logic

#### Methods:
- get_info() → returns a formatted summary string of the pet's details


### 3. Task
#### Attributes:
- name (str)
- task_type (str) — one of: "feeding", "walk", "medication", "appointment", "grooming", "training", "other"
- pet (Pet) — reference to the associated pet
- description (str)
- duration (float) — in hours
- priority (int) — e.g. 1 (highest) to 5 (lowest)
- frequency (str) — e.g. "daily", "weekly", "as_needed"
- preferred_time (int, optional) — preferred hour of day (0–23) to hint the scheduler
- is_completed (bool) — defaults to False

#### Methods:
- mark_complete() → sets is_completed = True
- reset() → sets is_completed = False (useful for recurring tasks)
- __str__() → returns a readable summary of the task


### 4. Scheduler
#### Attributes:
- owner (Owner) — single source of truth: gives access to tasks, pets, and availability
- schedule (dict) — generated output; e.g. {"Monday": [Task, Task, ...], ...}

#### Methods:
- generate_schedule() → builds a full weekly schedule across all pets, fitting tasks into the owner's availability windows; populates self.schedule
- get_schedule_for_pet(pet) → filters self.schedule to return only tasks for a specific pet
- get_combined_schedule() → returns self.schedule (all pets, full week)
- prioritize_tasks(tasks) → sorts a list of tasks by priority (and optionally by preferred_time); used internally by generate_schedule()
- display_schedule(pet=None) → prints the schedule to the CLI; if pet is provided, shows only that pet's tasks