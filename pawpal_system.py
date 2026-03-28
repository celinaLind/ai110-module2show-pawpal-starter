from dataclasses import dataclass, field
@dataclass
class Pet:
    name: str
    age: float
    species: str
    breed: str = None
    medical_notes: str = None

    def get_info(self):
        return f"{self.name} is a {self.age}-year-old {self.species} ({self.breed})."

@dataclass
class Task:
    name: str
    task_type: str
    pet: "Pet"
    description: str
    duration: float
    priority: int
    frequency: str
    preferred_time: int = None
    is_completed: bool = False

    def mark_completed(self):
        self.is_completed = True
    
    def reset(self):
        self.is_completed = False


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []
        self.availability: dict[str, tuple[str, int]] = {}  # e.g., {"Monday": ("09:00", 8)}

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_all_pets_info(self):
        return [pet.get_info() for pet in self.pets]

    def get_tasks_for_pet(self, pet_name: str):
        return [f"{task.description} - Due: {task.due_date} - Completed: {task.completed}" for task in self.tasks if pet_name in task.description]
    
    def get_tasks_info(self):
        return [f"{task.description} - Due: {task.due_date} - Completed: {task.completed}" for task in self.tasks]

    def update_availability(self, start_time: str, duration: int):
        # This is a placeholder implementation - you would need to implement the actual availability update logic
        pass


class Scheduler:
    def __init__(self):
        self.owners: Owner
        self.schedule: dict[str, list[Task]] = {}  # e.g., {"Monday": [Task1, Task2]}

    def generate_schedule(self):
        # This is a placeholder implementation - you would need to implement the actual scheduling logic
        pass

    def get_schedule_for_day(self, day: str):
        return self.schedule.get(day, [])
    
    def get_schedule_for_pet(self, pet_name: str, day: str):
        return [task for task in self.schedule.get(day, []) if pet_name in task.description]
    
    def display_schedule(self, day: str):
        tasks = self.get_schedule_for_day(day)
        return [f"{task.description} - Due: {task.due_date} - Completed: {task.completed}" for task in tasks]
    
    # May need to add more methods for weekly schedule

