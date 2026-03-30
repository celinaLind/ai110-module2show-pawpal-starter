# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


### Smarter Scheduling

The scheduler uses a greedy algorithm with gap-filling to build a weekly plan from the owner's availability windows.

**How tasks are sorted and placed:**
- Tasks with a `preferred_time` (anchored tasks) are placed at their requested time slot.
- Tasks without a `preferred_time` (flexible tasks) are sorted by priority and inserted into any open gaps before anchored tasks.
- If a gap is too small for a flexible task, it is placed after all anchored tasks instead.

**Recurring task handling:**
- `Daily` tasks are scheduled every day.
- `Weekly` and `One-time` tasks are scheduled only once across the full week using an ID-based deduplication set.

**Conflict detection:**
- The scheduler flags any anchored task that was pushed past its preferred start time.
- It also flags any task that runs past the end of the owner's availability window for that day.

**Filtering:**
- After generating a schedule, the UI lets you filter the view by pet name and/or completion status (All / Incomplete / Completed).
- Days with no matching tasks are hidden automatically.
