# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The PawPal+ System is broken down into 4 main classes: Owner, Pet, Task, and Scheduler. The owner houses the different pets along with the list of tasks that reference the specific pet they are for. The Pet class hold the standard information of a pet. The Task class allows user to update tasks, mark them as complete, and review task information. The Scheduler attributes the Owner class in order to utilize designated availability and task data to generate a daily schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, changes made due to:
* Dead/stale method references 
    - changed code during construction but forgot to remove all references
* Missing Relationships
    - Owner attribute for Scheduler was not properly assigned

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The schedule considers preferred time then priority then duration. I identified that when the owner wants to do the task is more important because they probably want to do it at that time for a specific reason. Priority is second in consideration for the obvious reason of being key in knowing if a task NEEDS to get done that day or could fall to another day. Finally duration provides the indicator of if said task will fit in allocated timeframe.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler makes a tradeoff by using two greedy passes rather than finding the mathematically optimal arrangement. First it selects tasks by preferred time and priority, then fills remaining gaps with flexible tasks in priority order. This means a suboptimal combination could slip through if a lower-priority task blocks a better fit later. This is reasonable for a pet care scenario because the owner's limited time should go toward the most important tasks first, and a predictable priority-based plan is more practical than exhaustively searching every possible arrangement.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
