# Step E-1: Deterministic Runtime Governance Validation via Neo4j (M2M Runtime Governance PoC)

## 1. Objective and Positioning: Proving Data-Driven Safety Interlocks

The objective of this step is to inject three dynamic telemetry streams from live plant environments into the knowledge graph compiled in Step D, formally verifying that **safety-critical access decisions and viewport actions execute deterministically without procedural if-else statements in application code**.

Historically, software systems hard-code domain rules directly into procedural application layers (e.g., Python, C#, or JavaScript):

- _"If user role is Operator, conceal disassembly instructions."_
- _"If residual hydraulic pressure exceeds 0.05 MPa, lock out disassembly and redirect to depressurization."_
- _"If machine serial corresponds to SP-X100, resolve the standard filter element."_

This PoC eliminates hard-coded logic by evaluating all business and safety rules directly as topological graph relationships. A single Cypher pattern traversal evaluates live constraints and returns deterministic authorization statuses alongside 3D HMI control signals in a structured JSON payload.

## 2. Directory Layout

Plaintext

```
01_Neo4j_M2M_PoC/
├── scenarios/
│   ├── scenario_matrix.md                   # Formal test case definitions (PoC1 through PoC6)
│   └── inputs/                              # Decoupled 3-stream telemetry payloads (JSON)
│       ├── sensor_state.json                # Dynamic sensor values (pressure, temperature)
│       ├── ui_event.json                    # Viewport pick events & requested step transitions
│       └── user_profile.json                # Certified operator/technician entitlements
├── runner/
│   ├── poc_runner.py                        # Single-scenario CLI test runner
│   └── batch_poc_runner.py                  # Automated batch execution harness (All 6 scenarios)
├── Evidence/
│   └── batch_test_results.log               # Verified console output logs (6/6 PASSED)
└── README.md                                # Step documentation
```

## 3. Decoupled Three-Stream Telemetry Model (Input Architecture)

Simulating an industrial cyber-physical deployment, system inputs are decoupled into three independent runtime telemetry streams before parameter injection into the Cypher evaluation query:

![](Pasted%20image%2020260926102440.png)

## 4. Test Scenario Matrix (PoC1–PoC6)

Six scenarios spanning foundational unit controls (featured in _tcworld online magazine_) to enterprise multi-interlocks (presented at _tcworld conference_) were designed and executed.

### ■ Stage 1: Core Safety Governance (Featured in _tcworld online magazine_)
Controlled comparative evaluations assessing deterministic gating across physical sensor thresholds and role entitlements.

| **Scenario** | **Evaluation Scope**                 | **3-Stream Injected Inputs**                                                     | **Expected Deterministic Assertion & HMI Action**                                                            |
| ------------ | ------------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **PoC1**     | **Role Entitlement Gate (Negative)** | ・Target: `STEP-007`<br>・Role: `iirds:Operator`<br>・Pressure: `0.0 MPa`           | ・Permitted: `false`<br>・Reason: `ERR_UNAUTHORIZED_ROLE`<br>・Action: `BLINK_RED` / Disassembly Locked Warning |
| **PoC2**     | **Pressure Interlock (Negative)**    | ・Target: `STEP-007`<br>・Role: `iirds:ServiceTechnician`<br>・Pressure: `0.5 MPa`  | ・Permitted: `false`<br>・Reason: `ERR_PRESSURE_REMAINING`<br>・Action: `BLINK_RED` / Route to Depressurization |
| **PoC3**     | **Authorized Clearance (Positive)**  | ・Target: `STEP-007`<br>・Role: `iirds:ServiceTechnician`<br>・Pressure: `0.02 MPa` | ・Permitted: `true`<br>・Reason: `SUCCESS`<br>・Action: `HIGHLIGHT_GREEN` / Advance Viewport Animation          |

### ■ Stage 2: Enterprise Complexity & Physical Multi-Interlocks (Featured at _tcworld conference_)
Multi-variant catalog compatibility, prerequisite tooling/PPE validation, and compound multi-sensor safety gates.

| **Scenario** | **Evaluation Scope**            | **3-Stream Injected Inputs**                                               | **Expected Deterministic Assertion & HMI Action**                                                                    |
| ------------ | ------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **PoC4**     | **Variant Compatibility**       | ・Target: `STEP-009`<br>・Variant: `SP-X100`<br>・Part: `FLT-STD-01`          | ・Permitted: `true`<br>・Reason: `MATCH_VARIANT_PART`<br>・Action: Highlight Verified Variant Element                   |
| **PoC5**     | **Tooling & PPE Verification**  | ・Target: `STEP-006`<br>・Tools: `TOOL-A`<br>・PPE: `Gloves, Eye Protection`  | ・Permitted: `true`<br>・Reason: `SUPPLIES_READY`<br>・Action: Release Task Execution Guidance                          |
| **PoC6**     | **Compound Physical Interlock** | ・Target: `STEP-006`<br>・Pressure: `0.5 MPa`<br>・Temp: `65°C` (Limit: 40°C) | ・Permitted: `false`<br>・Reason: `ERR_MULTIPLE_PHYSICAL_STATES`<br>・Action: Issue Aggregate Safety Interlock Override |

## 5. Automated Batch Test Execution and Verification

The automated test harness (`batch_poc_runner.py`) executes all six test scenarios sequentially against the live Neo4j database endpoint.

### Execution Log Trace

Plaintext

```
% python3 batch_poc_runner.py

============================================================
 PoC1 - PoC6 Knowledge Graph Batch Verification Runner
============================================================
[ PASS ] poc1_unauthorized_role
         Actual : Permitted=False, Code=ERR_UNAUTHORIZED_ROLE
[ PASS ] poc2_pressure_interlock
         Actual : Permitted=False, Code=ERR_PRESSURE_REMAINING
[ PASS ] poc3_normal_success
         Actual : Permitted=True, Code=SUCCESS
[ PASS ] poc4_variant_parts
         Actual : Permitted=True, Code=MATCH_VARIANT_PART
[ PASS ] poc5_required_tools
         Actual : Permitted=True, Code=SUPPLIES_READY
[ PASS ] poc6_multi_interlock
         Actual : Permitted=False, Code=ERR_MULTIPLE_PHYSICAL_STATES
============================================================
Execution Summary: 6/6 PASSED
============================================================

%
```

All six scenarios returned expected authorization flags, diagnostic reason codes, and viewport action triggers, confirming **100% deterministic conformance (6/6 PASSED)**. The raw audit trace is archived in `Evidence/batch_test_results.log`.

## 6. Architectural Implications and Engineering Significance

### ① Complete Elimination of Procedural Branching (`if-else` Blocks)
The Python execution client contains no procedural business logic or conditional safety assertions. Decision pathways are evaluated natively in Neo4j using pattern-matching traversals and Cypher `CASE` expressions.

When physical operating thresholds (e.g., maximum allowable pressure reduced to 0.03 MPa) or procedural prerequisites change, updates are confined entirely to knowledge graph assertions. **No application code refactoring, compilation, or redeployment is required.**

### ② Structural Hardware-Gated Safety Overrides
During hazard states (e.g., residual line pressure in PoC2 or combined thermal/pressure anomalies in PoC6), the system does not simply output warning text; it returns an explicit `Permitted: False` state paired directly with a red viewport flash command (`BLINK_RED`). Disassembly tasks remain structurally inaccessible until telemetry metrics fall within valid operational envelopes.

### ③ Direct Integration with Web3D (XVL) Runtimes
Responses are formatted as lightweight, schema-consistent JSON objects ready for client consumption via WebSocket or REST endpoints.

Front-end Web3D viewports consume the returned component identifiers and action tokens directly via JavaScript APIs, driving part highlighting, flashing alerts, and camera trajectories without intermediate translation layers.