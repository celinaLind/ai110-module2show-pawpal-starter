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

    def _is_eligible(self, task: Task, start_time: int, duration: int, scheduled_once: set) -> bool:
        """Returns True if a task should be considered for scheduling in a given availability window."""
        if task.frequency in ("Weekly", "One-time") and id(task) in scheduled_once:
            return False
        if task.is_completed and task.frequency == "One-time":
            return False
        if task.preferred_time is not None and not (start_time <= task.preferred_time < start_time + duration):
            return False
        return True

    def generate_schedule(self):
        """Builds a weekly schedule by matching tasks to the owner's availability windows."""
        scheduled_once = set()
        for day, (start_time, duration) in self.owner.availability.items():
            fitted, total = [], 0
            for pet in self.owner.pets:
                pet_tasks = [task for task in pet.tasks if self._is_eligible(task, start_time, duration, scheduled_once)]
                for task in self._prioritize_tasks(pet_tasks):
                    if total + task.duration <= duration:
                        fitted.append(task)
                        total += task.duration
                        if task.frequency in ("Weekly", "One-time"):
                            scheduled_once.add(id(task))
            self.schedule[day] = fitted
            self.assign_time(self.schedule[day], start_time)

    def assign_time(self, tasks: list[Task], start_time: int):
        """Assigns scheduled times, filling gaps before anchored tasks with flexible high-priority tasks."""
        anchored = [t for t in tasks if t.preferred_time is not None]
        flexible = [t for t in tasks if t.preferred_time is None]

        current_time = start_time
        flex_idx = 0

        for task in anchored:
            # fill gap before this anchored task with flexible tasks that fit
            while flex_idx < len(flexible):
                ft = flexible[flex_idx]
                if current_time + ft.duration <= task.preferred_time:
                    ft.scheduled_time = current_time
                    current_time += ft.duration
                    flex_idx += 1
                else:
                    break
            # schedule anchored task at its preferred time or current_time if we've passed it
            task.scheduled_time = max(current_time, task.preferred_time)
            current_time = task.scheduled_time + task.duration

        # schedule any remaining flexible tasks after all anchored tasks
        while flex_idx < len(flexible):
            flexible[flex_idx].scheduled_time = current_time
            current_time += flexible[flex_idx].duration
            flex_idx += 1

    def filter_schedule(self, pet_name: str = None, completed: bool = None):
        """Returns a filtered schedule by pet name and/or completion status. Pass None to skip that filter."""
        result = {}
        for day, tasks in self.schedule.items():
            filtered = []
            for task in tasks:
                if pet_name is not None and not any(task in pet.tasks for pet in self.owner.pets if pet.name == pet_name):
                    continue
                if completed is not None and task.is_completed != completed:
                    continue
                filtered.append(task)
            if filtered:
                result[day] = filtered
        return result

    def detect_conflicts(self):
        """Checks for anchored tasks pushed past their preferred time and tasks running past the availability window."""
        conflicts = []
        for day, tasks in self.schedule.items():
            start_time, duration = self.owner.availability[day]
            end_time = start_time + duration
            for task in tasks:
                if task.preferred_time is not None and task.scheduled_time > task.preferred_time:
                    conflicts.append(f"{day}: '{task.name}' wanted at {task.preferred_time}:00 but scheduled at {task.scheduled_time}:00")
                if task.scheduled_time + task.duration > end_time:
                    conflicts.append(f"{day}: '{task.name}' runs until {task.scheduled_time + task.duration}:00, past availability window ending at {end_time}:00")
        return conflicts

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

    def get_unscheduled_tasks(self):
        """Returns tasks that were not fit into any day of the schedule."""
        scheduled = {id(task) for tasks in self.schedule.values() for task in tasks}
        return [task for pet in self.owner.pets for task in pet.tasks if id(task) not in scheduled]

    def _prioritize_tasks(self, tasks: list[Task]):
        """Sorts anchored tasks (has preferred_time) by time, then flexible tasks by priority. Duration is the tiebreaker."""
        return sorted(tasks, key=lambda t: (t.preferred_time if t.preferred_time is not None else float("inf"), t.priority, t.duration))
