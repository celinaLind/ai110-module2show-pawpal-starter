import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
# add owner button
if st.button("Add Owner"):
    st.session_state.owner = Owner(owner_name)  # Store owner in session state for later use
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0.1, max_value=30.0, value=3.0)
# add pet button
if st.button("Add Pet"):
    st.session_state.owner.add_pet(Pet(name=pet_name, age=age, species=species))

# Get owner availability per day (for the week)
st.markdown("### Owner Availability")
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
preset_availability = {"Monday": (9, 4), "Tuesday": (9, 4), "Wednesday": (9, 4), "Thursday": (9, 4), "Friday": (9, 4), "Saturday": (10, 6), "Sunday": (10, 6)}
for day in days_of_week:
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.number_input(f"{day} start hour (0-23)", min_value=0, max_value=23, value=9, key=f"{day}_start")
    with col2:
        duration = st.number_input(f"{day} available hours", min_value=0, max_value=24, value=4, key=f"{day}_duration")
    if st.button(f"Set {day} availability"):
        st.session_state.owner.update_availability(day, start_time, duration)
    else:
        # Pre-fill with preset availability if not set
        if day not in st.session_state.owner.availability:
            st.session_state.owner.update_availability(day, *preset_availability[day])



st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    priority = {"low": 1, "medium": 2, "high": 3}[priority_label]
with col4:
    frequency = st.selectbox("Frequency", ["One-time", "Daily", "Weekly"], index=1)
with st.expander("More task details (optional)"):
    description = st.text_area("Description", value="")

if st.button("Add task"):
    st.session_state.owner.pets[0].add_task(
        Task(name=task_title, task_type="General", description=description, duration=int(duration)/60, priority=priority, frequency=frequency)
    )
    st.session_state.tasks.append({"Task": task_title, "Duration (hrs)": duration/60, "Priority": priority_label})

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.session_state.scheduler = Scheduler(st.session_state.owner)  # Create scheduler instance
    st.session_state.scheduler.generate_schedule()  # Populates self.schedule internally

    # Display the schedule in a more user-friendly way
    st.write("Schedule:")
    for day, tasks in st.session_state.scheduler.schedule.items():
        st.write(f"**{day}**:")
        for task in tasks:
            st.write(f"- {task.name} at {task.scheduled_time}:00 for {task.duration} hours (Priority: {task.priority})")

    unscheduled = st.session_state.scheduler.get_unscheduled_tasks()
    if unscheduled:
        st.warning(f"{len(unscheduled)} task(s) didn't fit into the schedule:")
        for task in unscheduled:
            st.write(f"- {task.name} ({task.duration} hrs, Priority: {task.priority})")

    conflicts = st.session_state.scheduler.detect_conflicts()
    if conflicts:
        st.error(f"{len(conflicts)} scheduling conflict(s) detected:")
        for conflict in conflicts:
            st.write(f"- {conflict}")

