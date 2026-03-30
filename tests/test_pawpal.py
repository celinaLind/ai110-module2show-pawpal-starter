from pawpal_system import Owner, Pet, Task


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
