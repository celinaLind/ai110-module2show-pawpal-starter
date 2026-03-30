from pawpal_system import Owner, Pet, Task, Scheduler

# Example usage
if __name__ == "__main__":
    owner = Owner("Alice")
    pet1 = Pet(name="Buddy", age=5, species="Dog", breed="Labrador")
    pet2 = Pet(name="Mittens", age=3, species="Cat")

    # Tasks added out of order (preferred_times: 12, 9, 11, no preferred_time)
    task1 = Task(name="Afternoon Nap Setup", task_type="Rest", description="Set up Buddy's nap area.", duration=0.5, priority=2, frequency="Daily", preferred_time=12)
    task2 = Task(name="Morning Walk", task_type="Exercise", description="Take Buddy for a walk in the park.", duration=1, priority=1, frequency="Daily", preferred_time=9)
    task3 = Task(name="Midday Check-in", task_type="Enrichment", description="Play with Buddy.", duration=0.5, priority=2, frequency="Daily", preferred_time=11)
    task4 = Task(name="Vet Visit", task_type="Health Check", description="Take Buddy to the vet.", duration=2, priority=1, frequency="One-time")
    task5 = Task(name="Feeding", task_type="Feeding", description="Feed Mittens her breakfast.", duration=0.5, priority=1, frequency="Daily", preferred_time=9)

    # Added out of order: task1 (12:00), task3 (11:00), task2 (9:00), task4 (no time), task5 (9:00)
    pet1.add_task(task1)
    pet1.add_task(task3)
    pet1.add_task(task2)
    pet1.add_task(task4)
    pet2.add_task(task5)

    print(pet1.get_info())
    print(pet2.get_info())

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    owner.update_availability("Monday", 9, 5)
    owner.update_availability("Tuesday", 9, 5)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    # Full schedule (sorted by time via assign_time)
    print("\n--- Full Schedule ---")
    scheduler.display_schedule()

    # Filter: Buddy's tasks only
    print("\n--- Buddy's Tasks Only ---")
    buddy_schedule = scheduler.filter_schedule(pet_name="Buddy")
    for day, tasks in buddy_schedule.items():
        print(f"{day}:")
        for task in tasks:
            print(f"  {task.scheduled_time}:00 - {task.name} ({task.duration}h, Priority: {task.priority})")

    # Filter: incomplete tasks only
    print("\n--- Incomplete Tasks Only ---")
    incomplete = scheduler.filter_schedule(completed=False)
    for day, tasks in incomplete.items():
        print(f"{day}:")
        for task in tasks:
            print(f"  {task.scheduled_time}:00 - {task.name}")

    # Unscheduled tasks
    unscheduled = scheduler.get_unscheduled_tasks()
    if unscheduled:
        print(f"\n--- Unscheduled Tasks ({len(unscheduled)}) ---")
        for task in unscheduled:
            print(f"  - {task.name} ({task.duration}h, Priority: {task.priority})")

    # Conflicts
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print(f"\n--- Conflicts ({len(conflicts)}) ---")
        for conflict in conflicts:
            print(f"  - {conflict}")
    else:
        print("\nNo scheduling conflicts.")
