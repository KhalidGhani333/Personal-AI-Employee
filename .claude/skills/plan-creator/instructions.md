# Plan Creator - Detailed Instructions

## Objective
Transform complex tasks into detailed, actionable execution plans with clear steps, dependencies, and success criteria.

## Plan Creation Workflow

### 1. Analyze Task
```
Input: Complex task description
Process:
  - Identify main objective
  - List requirements
  - Identify constraints
  - Determine success criteria
  - Estimate complexity
```

### 2. Break Down into Steps

**Decomposition Strategy:**
```
1. Identify major phases
2. Break each phase into tasks
3. Break tasks into subtasks
4. Ensure each step is actionable
5. Add verification checkpoints
```

**Example:**
```
Task: "Launch new product feature"

Phases:
1. Planning & Design
2. Development
3. Testing
4. Deployment
5. Monitoring

Phase 1 - Planning & Design:
- [ ] Define feature requirements
- [ ] Create user stories
- [ ] Design UI mockups
- [ ] Review with stakeholders
- [ ] Finalize specifications
```

### 3. Identify Dependencies

**Dependency Types:**
- **Sequential**: Step B requires Step A completion
- **Parallel**: Steps can run simultaneously
- **Conditional**: Step depends on outcome of previous step

**Notation:**
```
- [ ] Step 1 (no dependencies)
- [ ] Step 2 (depends on: Step 1)
- [ ] Step 3 (depends on: Step 1)
- [ ] Step 4 (depends on: Step 2, Step 3)
```

### 4. Create Plan File

```markdown
---
type: execution_plan
task: {task_title}
created: {ISO_timestamp}
status: pending|in_progress|completed
priority: high|normal|low
estimated_duration: {duration}
---

# Execution Plan: {Task Title}

## Objective
{clear_statement_of_goal}

## Success Criteria
- [ ] {criterion_1}
- [ ] {criterion_2}
- [ ] {criterion_3}

## Prerequisites
- {prerequisite_1}
- {prerequisite_2}

## Constraints
- {constraint_1}
- {constraint_2}

## Execution Steps

### Phase 1: {Phase Name}
**Duration**: {estimated_time}
**Dependencies**: None

- [ ] Step 1.1: {description}
  - Action: {specific_action}
  - Expected Output: {output}
  - Verification: {how_to_verify}

- [ ] Step 1.2: {description}
  - Action: {specific_action}
  - Expected Output: {output}
  - Verification: {how_to_verify}

### Phase 2: {Phase Name}
**Duration**: {estimated_time}
**Dependencies**: Phase 1 complete

- [ ] Step 2.1: {description}
- [ ] Step 2.2: {description}

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk_1} | High | {mitigation_strategy} |
| {risk_2} | Medium | {mitigation_strategy} |

## Resources Required
- {resource_1}
- {resource_2}

## Rollback Plan
If things go wrong:
1. {rollback_step_1}
2. {rollback_step_2}

## Progress Tracking
- Started: {timestamp}
- Current Phase: {phase_name}
- Completion: {percentage}%
- Estimated Completion: {date}

## Notes
{any_additional_notes}
```

### 5. Ralph Wiggum Loop Integration

**For Autonomous Execution:**
```markdown
## Completion Promise
When all steps are complete, output:
<promise>PLAN_COMPLETE</promise>

## Current Status
- Total Steps: {total}
- Completed: {completed}
- Remaining: {remaining}
- Next Step: {next_step_description}
```

### 6. Track Progress

**Update Plan File:**
```
- Mark completed steps with [x]
- Update Current Phase
- Update Completion percentage
- Add notes on blockers
- Update estimated completion
```

## Plan Templates

### Software Development Plan
```markdown
## Phase 1: Requirements
- [ ] Gather requirements
- [ ] Create specifications
- [ ] Review with stakeholders

## Phase 2: Design
- [ ] Create architecture diagram
- [ ] Design database schema
- [ ] Design API endpoints

## Phase 3: Implementation
- [ ] Set up development environment
- [ ] Implement core features
- [ ] Write unit tests

## Phase 4: Testing
- [ ] Run unit tests
- [ ] Perform integration testing
- [ ] User acceptance testing

## Phase 5: Deployment
- [ ] Deploy to staging
- [ ] Final testing
- [ ] Deploy to production
```

### Business Process Plan
```markdown
## Phase 1: Analysis
- [ ] Identify current process
- [ ] Document pain points
- [ ] Define improvement goals

## Phase 2: Design
- [ ] Design new process
- [ ] Create workflow diagram
- [ ] Define metrics

## Phase 3: Implementation
- [ ] Train team
- [ ] Roll out new process
- [ ] Monitor adoption

## Phase 4: Optimization
- [ ] Collect feedback
- [ ] Measure metrics
- [ ] Refine process
```

### Marketing Campaign Plan
```markdown
## Phase 1: Strategy
- [ ] Define target audience
- [ ] Set campaign goals
- [ ] Determine budget

## Phase 2: Content Creation
- [ ] Create content calendar
- [ ] Design visuals
- [ ] Write copy

## Phase 3: Execution
- [ ] Schedule posts
- [ ] Launch campaign
- [ ] Monitor engagement

## Phase 4: Analysis
- [ ] Collect metrics
- [ ] Analyze results
- [ ] Generate report
```

## Complexity Assessment

**Simple Task (No plan needed):**
- Single step
- No dependencies
- < 1 hour duration

**Medium Task (Basic plan):**
- 3-5 steps
- Few dependencies
- 1-4 hours duration

**Complex Task (Detailed plan):**
- 6+ steps
- Multiple dependencies
- > 4 hours duration
- Multiple phases

## Integration Points

- **Task Manager**: Create tasks from plan steps
- **Dashboard Updater**: Update plan progress
- **Log Manager**: Log plan execution
- **Approval Handler**: Request approval for risky steps

## Success Criteria
- All steps clearly defined
- Dependencies identified
- Success criteria measurable
- Plan executable by AI or human
- Progress trackable
