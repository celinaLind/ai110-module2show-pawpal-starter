from pawpal_system import Owner, Pet, Task, Scheduler

# Example usage
if __name__ == "__main__":
    owner = Owner("Alice")
    pet1 = Pet(name="Buddy", age=5, species="Dog", breed="Labrador")
    pet2 = Pet(name="Mittens", age=3, species="Cat")

    task1 = Task(name="Morning Walk", task_type="Exercise", description="Take Buddy for a walk in the park.", duration=1, priority=1, frequency="Daily", preferred_time=9)
    task2 = Task(name="Feeding", task_type="Feeding", description="Feed Mittens her breakfast.", duration=0.5, priority=2, frequency="Daily", preferred_time=9)
    task3 = Task(name="Vet Visit", task_type="Health Check", description="Take Buddy to the vet for a check-up.", duration=2, priority=1, frequency="Monthly")

    pet1.add_task(task1)
    pet1.add_task(task3)
    pet2.add_task(task2)

    # confirm pet info
    print(pet1.get_info())
    print(pet2.get_info())

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    owner.update_availability("Monday", 9, 4)
    owner.update_availability("Tuesday", 9, 4)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    scheduler.display_schedule()
