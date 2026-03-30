from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task(name="Morning Walk", task_type="Exercise", description="Walk in the park", duration=1, priority=1, frequency="Daily")
    task.mark_complete()
    assert task.is_completed == True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Buddy", age=5, species="Dog")
    task = Task(name="Feeding", task_type="Feeding", description="Feed Buddy", duration=0.5, priority=2, frequency="Daily")
    pet.add_task(task)
    task2 = Task(name="Vet Visit", task_type="Health Check", description="Take Buddy to the vet", duration=2, priority=1, frequency="Monthly")
    pet.add_task(task2)
    assert len(pet.tasks) == 2


def test_one_time_task_scheduled_only_once():
    """A One-time task should appear in the schedule on only one day across a multi-day week."""
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", age=2, species="Cat")
    task = Task(name="Vet Visit", task_type="Health Check", description="Annual checkup", duration=1, priority=1, frequency="One-time")
    pet.add_task(task)
    owner.add_pet(pet)
    owner.update_availability("Monday", 9, 4)
    owner.update_availability("Tuesday", 9, 4)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    days_with_task = [day for day, tasks in scheduler.schedule.items() if task in tasks]
    assert len(days_with_task) == 1


def test_tasks_sorted_by_preferred_time():
    """Tasks added out of order should be scheduled in chronological order by preferred_time."""
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", age=2, species="Cat")
    task_noon = Task(name="Midday Feed", task_type="Feeding", description="", duration=0.5, priority=1, frequency="Daily", preferred_time=12)
    task_morning = Task(name="Morning Walk", task_type="Exercise", description="", duration=0.5, priority=1, frequency="Daily", preferred_time=9)
    task_mid = Task(name="Play Time", task_type="Enrichment", description="", duration=0.5, priority=1, frequency="Daily", preferred_time=11)
    # Added out of order
    pet.add_task(task_noon)
    pet.add_task(task_morning)
    pet.add_task(task_mid)
    owner.add_pet(pet)
    owner.update_availability("Monday", 9, 5)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    times = [t.scheduled_time for t in scheduler.schedule["Monday"]]
    assert times == sorted(times)


def test_flexible_task_fills_gap_before_anchored_task():
    """A high-priority flexible task should be placed in a gap before an anchored task, not after."""
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", age=2, species="Cat")
    anchored = Task(name="Vet Visit", task_type="Health Check", description="", duration=1, priority=2, frequency="Daily", preferred_time=11)
    flexible = Task(name="Brush", task_type="Grooming", description="", duration=1, priority=1, frequency="Daily")
    pet.add_task(anchored)
    pet.add_task(flexible)
    owner.add_pet(pet)
    owner.update_availability("Monday", 9, 4)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    assert flexible.scheduled_time == 9


def test_overflow_tasks_appear_as_unscheduled():
    """Tasks that exceed the available time window should be returned by get_unscheduled_tasks()."""
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", age=2, species="Cat")
    task1 = Task(name="Walk", task_type="Exercise", description="", duration=2, priority=1, frequency="Daily")
    task2 = Task(name="Groom", task_type="Grooming", description="", duration=2, priority=2, frequency="Daily")
    task3 = Task(name="Play", task_type="Enrichment", description="", duration=2, priority=3, frequency="Daily")
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    owner.add_pet(pet)
    owner.update_availability("Monday", 9, 3)  # Only 3 hours — fits task1 and task2 but not task3

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    unscheduled = scheduler.get_unscheduled_tasks()
    assert task3 in unscheduled


def test_conflict_detected_when_tasks_share_preferred_time():
    """When two anchored tasks share the same preferred_time, the second should be flagged as a conflict."""
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", age=2, species="Cat")
    task1 = Task(name="Walk", task_type="Exercise", description="", duration=1, priority=1, frequency="Daily", preferred_time=9)
    task2 = Task(name="Feed", task_type="Feeding", description="", duration=1, priority=2, frequency="Daily", preferred_time=9)
    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)
    owner.update_availability("Monday", 9, 4)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0
