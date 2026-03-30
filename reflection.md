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

AI was used like a pair-programmer throughout this projects. For instance I came up with the initial scaffolding of classes and asked AI to help me flush out missing methods or different ways to consider references. Then AI was utilized if I got stuck on a bug or came across an error I haven't seen before. And instead of asking the agent to fix the issue, I would ask it to explain why the behavior was happening. Finally, I utilized it to quickly document and summarize the codebase.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When designing the task sorting logic, the initial approach assigned a value of infinity to any task without a preferred_time, which caused all flexible tasks to be scheduled after every anchored task. I identified a flaw in this approach: if two anchored tasks had a gap between them, that open time would go unused even if a flexible task could fit perfectly inside it. I proposed that flexible tasks should instead fill gaps between anchored tasks rather than always being placed at the end, which led to the two-pass assign_time design where flexible tasks are inserted into available gaps before each anchored task and only deferred to the end if no gap fits them.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

1. Marking a task complete updates its status
    * `mark_complete` is the primary way task state changes, so verifying it works correctly prevents silent failures when tracking progress.
2. Adding tasks to a pet increases that pet's task count
    * `add_task` is the entry point for all scheduling data, so a broken count means the scheduler is working with incomplete information.
3. A One-time task only appears in the schedule once across a multi-day week
    * Without deduplication, a One-time task like a vet visit would repeat every day, which defeats its purpose entirely.
4. Tasks added out of order are scheduled in chronological order by preferred time
    * The scheduler receives tasks in whatever order the user adds them, so correct chronological output proves the sorting logic works regardless of input order.
5. A flexible task fills an open gap before an anchored task rather than being pushed to the end
    * Gap-filling is the core efficiency feature of `assign_time`. If it fails, high-priority flexible tasks get pushed to the end and available time goes to waste.
6. Tasks that exceed the available time window surface in get_unscheduled_tasks()
    * Tasks that silently don't fit would leave the owner unaware that part of their pet's care plan was dropped.
7. Two tasks sharing the same preferred time triggers a conflict detection warning
    * Conflict detection is the scheduler's way of communicating when it cannot honor a requested time, which is critical feedback for the owner to adjust their plan.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Out of 10, I would say my confidence in my scheduler is a 9. Now, there are still kinks and maybe a better strategy for the sorts but it works and provides the owner with an adequate schedule for each pet. Some edge cases I would consider are tasks that need to be done multiple times a day, day of availability changes, and tasks user is able to do simultaneously.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Getting more experience with pytests.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would have started simpler, during the design phase I was thinking as if this was a version 4 product when I should have been considering the MVP instead. This caused me to spend more time than necessary setting up functions reiterating, retesting, and didn't allow for adequate time to finalize the product. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Start with the MVP and expand from there.

I forgot to add the recurrence logic behavior: Daily tasks are re-scheduled each day but there's no logic that marks a daily task complete and automatically creates a new instance for the next day. The reset() method exists on Task but nothing calls it automatically.
