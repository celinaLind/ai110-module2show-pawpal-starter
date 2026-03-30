from dataclasses import dataclass, field

@dataclass
class Task:
    name: str
    task_type: str
    description: str
    duration: float
    priority: int
    frequency: str
    preferred_time: int = None
    scheduled_time: int = None
    is_completed: bool = False

    def mark_complete(self):
        """Marks the task as completed."""
        self.is_completed = True

    def reset(self):
        """Resets the task to incomplete, useful for recurring tasks."""
        self.is_completed = False


@dataclass
class Pet:
    name: str
    age: float
    species: str
    breed: str = None
    medical_notes: str = None
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Removes a task from this pet's task list."""
        self.tasks.remove(task)

    def get_info(self):
        """Returns a formatted summary of the pet's details."""
        return f"{self.name} is a {self.age}-year-old {self.species} ({self.breed})."


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.availability: dict[str, tuple[int, int]] = {}  # e.g., {"Monday": (9, 4)}

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_tasks_for_pet(self, pet: Pet):
        """Returns the task list for a specific pet."""
        return pet.tasks

    def update_availability(self, day: str, start_time: int, duration: int):
        """Sets the owner's available window for a given day as (start_hour, duration_in_hours)."""
        self.availability[day] = (start_time, duration)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: dict[str, list[Task]] = {}  # e.g., {"Monday": [Task, Task, ...]}

    def generate_schedule(self):
        """Builds a weekly schedule by matching tasks to the owner's availability windows."""
        for day, (start_time, duration) in self.owner.availability.items():
            daily_tasks = []
            for pet in self.owner.pets:
                daily_tasks.extend([task for task in pet.tasks if task.preferred_time == start_time])
            self.schedule[day] = self._prioritize_tasks(daily_tasks)[:duration]
            self.assign_time(self.schedule[day], start_time)

    def assign_time(self, tasks: list[Task], start_time: int):
        """Assigns a sequential scheduled_time to each task based on the start time and durations."""
        current_time = start_time
        for task in tasks:
            task.scheduled_time = current_time
            current_time += task.duration

    def get_schedule_for_pet(self, pet: Pet):
        """Returns a filtered schedule containing only tasks belonging to the given pet."""
        return {day: [task for task in tasks if task in pet.tasks] for day, tasks in self.schedule.items()}

    def display_schedule(self, pet: Pet = None):
        """Prints the schedule to the CLI. If a pet is provided, shows only that pet's tasks."""
        if pet:
            schedule = self.get_schedule_for_pet(pet)
            print(f"Schedule for {pet.name}:")
        else:
            schedule = self.schedule
            print("Combined Schedule for All Pets:")

        for day, tasks in schedule.items():
            print(f"{day}:")
            for task in tasks:
                print(f" {task.scheduled_time} - {task.name} ({task.task_type}): {task.description} [Duration: {task.duration}h, Priority: {task.priority}]")

    def _prioritize_tasks(self, tasks: list[Task]):
        """Sorts tasks by priority then duration (lowest values first)."""
        return sorted(tasks, key=lambda t: (t.priority, t.duration))

    def get_combined_schedule(self):
        """Returns the full schedule across all pets."""
        combined_tasks = {
            day: [task for task in tasks if task in pet.tasks]
            for day, tasks in self.schedule.items()
            for pet in self.owner.pets
        }
        return combined_tasks
