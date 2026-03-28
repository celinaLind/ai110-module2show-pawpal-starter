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
    is_completed: bool = False

    def mark_complete(self):
        self.is_completed = True

    def reset(self):
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
        self.tasks.append(task)

    def remove_task(self, task: Task):
        self.tasks.remove(task)

    def get_info(self):
        return f"{self.name} is a {self.age}-year-old {self.species} ({self.breed})."


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.availability: dict[str, tuple[int, int]] = {}  # e.g., {"Monday": (9, 4)}

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def get_tasks_for_pet(self, pet: Pet):
        return pet.tasks

    def update_availability(self, day: str, start_time: int, duration: int):
        self.availability[day] = (start_time, duration)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: dict[str, list[Task]] = {}  # e.g., {"Monday": [Task, Task, ...]}

    def generate_schedule(self):
        pass

    def get_schedule_for_pet(self, pet: Pet):
        return {day: [task for task in tasks if task in pet.tasks] for day, tasks in self.schedule.items()}

    def display_schedule(self, pet: Pet = None):
        pass
