"""
Time: The Undefined Parameter — Simulation Code
Author: Jerry Z. Xie
Affiliation: The Silicon Valley Research, Inc.
Paper: Time: The Undefined Parameter: Toward a Relational Construction of Temporal Order

This script simulates the core relational framework of the paper:
- Events as transitions between distinguishable states
- A causal partial order (assumed as a physical consistency condition)
- Persistent records as recoverable mutual information between event states
- An observer who reconstructs temporal order from accessible records
- A numerical clock parametrization of that reconstructed order

The purpose is to demonstrate that temporal order can be constructed from
relational structure without a pre-existing time parameter.
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

print("=" * 70)
print("Time: The Undefined Parameter — Computational Demonstration")
print("=" * 70)

# 1. Generate a finite set of events
# Each event is a tuple (state_before, state_after) where state is an integer.
# Distinguishable states mean state_before != state_after.

def generate_events(n_events=8, n_states=10):
    """Generate a set of distinguishable events."""
    events = []
    for _ in range(n_events):
        s_i = np.random.randint(0, n_states)
        s_j = np.random.randint(0, n_states)
        while s_j == s_i:
            s_j = np.random.randint(0, n_states)
        events.append((s_i, s_j))
    return events

events = generate_events(n_events=8)
print("\n1. Events (transitions between distinguishable states):")
for i, (s_i, s_j) in enumerate(events):
    print(f"   E{i}: S_{s_i} -> S_{s_j}")

# 2. Define a causal relation (strict partial order)
# We assign a causal relation as a consistency assumption.
# For this simulation, we define a fixed partial order: events are causally ordered
# by their index, i.e., E_i causally precedes E_j if i < j.
# This is an assumption, not derived from distinguishability.

def is_causal(e_i, e_j):
    """Assumed causal relation: E_i can influence E_j if i < j."""
    return e_i < e_j

print("\n2. Causal order (assumed as physical consistency condition):")
print("   E_i precedes E_j if i < j.")
for i, j in combinations(range(len(events)), 2):
    if is_causal(i, j):
        print(f"   E{i} -> E{j} (causal precedence)")

# 3. Persistent records: mutual information between event states
# We define a record as I(degrees_of_freedom_A; degrees_of_freedom_B) > I_min
# Here we simulate this using a simple correlation between event states.
# For each pair of events, we compute a proxy "mutual information" based on
# the overlap of their source/destination states.

def record_exists(e_i, e_j, threshold=0.5):
    """Simulate persistent record via mutual information between states."""
    # Simple proxy: record exists if the states share some structure.
    # This is a simplified correlation, not actual mutual information.
    si, sj = e_i
    sk, sl = e_j
    # Overlap between the two events (shared state values)
    overlap = len(set((si, sj)).intersection(set((sk, sl))))
    prob = overlap / 4.0  # normalized to 0-1
    return prob > threshold

print("\n3. Persistent records (I(S_A; S_B) > I_min):")
record_matrix = np.zeros((len(events), len(events)))
for i in range(len(events)):
    for j in range(len(events)):
        if i != j and record_exists(events[i], events[j], threshold=0.3):
            record_matrix[i, j] = 1
            print(f"   E{i} -> E{j}: record exists (I > I_min)")

# 4. Observer as a physical subsystem with internal records
# The observer has access only to events for which it has stored a record.

observer_accessible = set()
for i in range(len(events)):
    for j in range(len(events)):
        if record_matrix[i, j] == 1:
            observer_accessible.add(i)
            observer_accessible.add(j)

observer_accessible = sorted(observer_accessible)
print(f"\n4. Observer-accessible events: {observer_accessible}")

# 5. Temporal order for the observer: restriction of causal order to accessible events
# Temporal order: E_i precedes E_j if they are both accessible and causally related.

def is_temporal_order(i, j, accessible):
    """Temporal order: restriction of causal order to accessible events."""
    if i not in accessible or j not in accessible:
        return False
    return is_causal(i, j)

print("\n5. Temporal order (reconstructed by observer):")
for i in observer_accessible:
    for j in observer_accessible:
        if i != j and is_temporal_order(i, j, observer_accessible):
            print(f"   E{i} -> E{j} (temporal order)")

# 6. Clock time: monotonic numerical parametrization of temporal order
# Assign a real number tau(E) such that if E_i precedes E_j, then tau(E_i) < tau(E_j).
# This is a representation, not the order itself.

def assign_clock_time(accessible_events):
    """Assign a clock time that is order-preserving."""
    # Simple mapping: use event indices but ensure consistency with causal order.
    tau = {}
    # For accessible events, assign a value that respects order.
    # We use a topological sorting approximation: just use sorted order.
    for idx, e in enumerate(sorted(accessible_events)):
        tau[e] = idx + 1.0
    return tau

tau = assign_clock_time(observer_accessible)
print("\n6. Clock time (monotonic numerical representation):")
for e in sorted(tau.keys()):
    print(f"   tau(E{e}) = {tau[e]}")

# 7. Verification: check that clock time respects temporal order
print("\n7. Verification: Does clock time preserve temporal order?")
valid = True
for i in observer_accessible:
    for j in observer_accessible:
        if i != j and is_temporal_order(i, j, observer_accessible):
            if tau[i] >= tau[j]:
                print(f"   ERROR: E{i} precedes E{j} but tau({i})={tau[i]} >= tau({j})={tau[j]}")
                valid = False
if valid:
    print("   ✅ All temporal order relations are preserved by clock time.")
    print("   tau is a valid representation of temporal order.")

print("\n" + "=" * 70)
print("Demonstration complete.")
print("The simulation shows that temporal order can be constructed from")
print("relational structure (events, causal order, records) and that a")
print("numerical clock time can be assigned as a monotonic parametrization,")
print("without assuming a pre-existing time parameter.")
print("=" * 70)