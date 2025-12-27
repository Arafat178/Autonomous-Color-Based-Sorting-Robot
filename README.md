# Autonomous Color-Based Sorting Robot

### A Deterministic Pick-and-Place System using RoboDK & Python

📺 **Project Demonstration (YouTube):**
[https://youtu.be/_ClDFjRHCIg](https://youtu.be/_ClDFjRHCIg)

---

##  What This Project *Actually* Is

This project simulates an **industrial robotic sorting cell** where a 6-DOF robotic arm autonomously picks randomly distributed objects and sorts them into organized locations based on color.

There is **no vision system**, **no ROS**, and **no manual teaching**.
Every decision — where to move, what to pick, where to place — is made programmatically.

The goal is not visual realism.
The goal is **logical correctness and motion intent**.

---

## Why This Problem Matters

In real factories, robots often:

* Receive parts in **unordered positions**
* Must **avoid collisions**
* Must **sort or palletize** items based on attributes
* Must move safely using approach and retreat strategies

This project models that exact workflow — in simulation — using deterministic logic.

---

## System Description (From Zero)

### 1️⃣ The Environment

The simulation contains:

* A fixed work table
* 10 identical box objects
* A 6-axis collaborative robot
* A parallel gripper tool

At runtime:

* Boxes do **not start in predefined locations**
* Their positions are **randomized within workspace limits**
* Overlapping placements are prevented mathematically

This mimics a messy, real-world input scenario.

---

### 2️⃣ Randomized but Valid Object Placement

Each box is assigned a random `(x, y)` position.

Before placement, the algorithm checks:

* Distance from every previously placed box
* Ensures a minimum spacing (`BOX_SIZE`)

```python
if abs(rand_x - px) < BOX_SIZE and abs(rand_y - py) < BOX_SIZE:
    overlap = True
```

This is a simplified form of **collision-aware spatial allocation**, similar to bin-packing logic.

---

### 3️⃣ Color as Semantic Information

Each box is assigned **one of three colors**:

* Red
* Green
* Blue

The robot does **not “see”** the color.
Instead, color is treated as **known object metadata**, which is common in structured industrial workflows.

This avoids artificial AI complexity and keeps the system deterministic.

---

### 4️⃣ Decision Logic: How the Robot Thinks

For each box:

1. Read its pose (position in space)
2. Read its color
3. Decide **which sorting zone** it belongs to
4. Compute a **unique placement position** using counters
5. Execute pick-and-place motion

This makes the robot’s behavior:

* Predictable
* Repeatable
* Debuggable

No magic. Only logic.

---

##  Motion Planning Philosophy

Two motion types are used intentionally:

### 🔹 MoveJ (Joint Space)

Used when:

* Moving between distant locations
* Collision risk is low
* Speed and flexibility are preferred

### 🔹 MoveL (Linear Space)

Used when:

* Approaching an object
* Grasping
* Placing

This reflects **real industrial programming standards**.

---

###  Safe Approach & Retreat

The robot never dives straight into an object.

Every pick/place follows this structure:

1. Move above the target (`+150 mm`)
2. Linear descent
3. Grasp / release
4. Linear retreat
5. Move away safely

This prevents accidental collisions and reflects good robotic practice.

---

##  Object Attachment (Real Kinematics)

When a box is picked:

```python
target_box.setParentStatic(gripper)
```

This means:

* The box becomes part of the robot’s kinematic chain
* It moves exactly as the tool moves

When released:

```python
target_box.setParentStatic(table)
```

This is **true grasp simulation**, not animation.

---

##  Sorting Strategy Explained Clearly

The workspace contains **three target zones**:

| Color | Y-Position | Meaning             |
| ----- | ---------- | ------------------- |
| Red   | −200       | Left sorting lane   |
| Green | 0          | Center sorting lane |
| Blue  | +200       | Right sorting lane  |

Each placed box is offset in X using a counter to prevent overlap.

This mimics **organized palletizing**, not random dumping.

---

##  Full Execution Flow

1. Initialize RoboDK connection
2. Load robot, gripper, tool, and table
3. Randomly place boxes without overlap
4. Move robot to home position
5. Loop through all boxes:

   * Read pose
   * Identify color
   * Compute pick & place targets
   * Execute motion
6. Return robot to home

No manual intervention.

---

## ⚙️ Tools & Technologies

* **Python 3**
* **RoboDK Simulation Software**
* **RoboDK Python API**
* Rigid-body kinematics
* Coordinate frame transformations

---

##  Known Limitations (Explicitly Stated)

* Inverse kinematics handled internally by RoboDK
* No sensor feedback
* No real-time collision re-planning
* Simulation-only (no hardware deployment)

These are **design boundaries**, not mistakes.

---

##  Future Expansion (Research Direction)

This project is intentionally structured so it can evolve into:

* Custom analytical or numerical IK solver
* Collision-aware trajectory planning
* SolidWorks-to-RoboDK automation
* Vision-based sorting (OpenCV)
* ANSYS-based gripper force validation
* Real-robot deployment

---

##  Demo Video

 Watch the robot in action:
[https://youtu.be/_ClDFjRHCIg](https://youtu.be/_ClDFjRHCIg)

---

##  Author

**Arafat**
Mechanical Engineering Student
