# Step B: Automated Decomposition of Technical Documentation into iiRDS Atomic Step JSON

## 1. Objective and Positioning: Deconstructing Narrative Manuals into Minimum Executable Units

Conventional technical documentation is written for human interpretation, routinely conflating operational prerequisites, safety warnings, physical part references, and product variant branches within a single paragraph.

To dynamically link procedural guidance with real-time industrial IoT telemetry and 3D CAD runtime viewports (e.g., XVL camera trajectories and part highlights), narrative text must be decomposed into **"one-operation, one-assertion" executable nodes (Atomic Steps)**, with implicit domain constraints extracted into structured metadata (Lifted Metadata).

This step establishes an automated extraction and quality-audit pipeline that eliminates LLM hallucinations (such as unconstrained tag fabrication), outputting schema-compliant **iiRDS (intelligent information Request and Delivery Standard)** JSON records ready for direct ingestion into Neo4j.

## 2. Directory Layout

Plaintext

```
Step_B_Manual_to_iiRDS/
├── 01_Input/
│   └── MAN-HYD-2026-01.md                   # Source input: Unstructured hydraulic maintenance manual
├── 02_Prompt/
│   ├── prompt_manual_to_iirds.md            # Schema-driven atomic decomposition prompt
│   └── prompt_audit_iirds.md                # Independent 5-axis automated audit prompt
├── 03_Output/
│   └── iirds_atomic_data.json               # Artifact: Structured iiRDS Atomic Step JSON (10 Steps)
├── 04_Audit/
│   └── audit_result_iirds.json              # Automated audit log (Score: 1.0 PASSED)
└── README.md                                # Step documentation
```

## 3. Execution Pipeline (4-Phase Architecture)

To ensure strict determinism and reproducibility, the decomposition pipeline executes across four discrete phases:

![](Pasted%20image%2020260926100504.png)


### Phase 1: Canonical Vocabulary Specification (Whitelist Enforcement)
Constrains output entities to formal taxonomy classes defined in the official iiRDS specification (`iiRDS_core.ttl`):
- `TargetAudience`: `iirds:Operator`, `iirds:ServiceTechnician`
- `ActionType`: `Disassembly`, `Replacement`, `Depressurization`, `Inspection`, `Operation`, `Tightening`, `Contact`, `Disposal`
- Domain extensions (`ext:PhysicalState`) explicitly capture physical operating states (line pressure, fluid temperature, valve status) to govern runtime safety interlocks.

### Phase 2: Schema-Driven Prompt Engineering
Injects formal iiRDS semantic classes (`iirds:`) directly into output property definitions and type specifications within the JSON Schema. Explicit slots for physical parameters (`required_physical_states`) and negative prohibitions (`prohibited_action`) prevent uncontrolled narrative escape.

### Phase 3: Atomic Step Extraction
Processes source technical documentation (`MAN-HYD-2026-01.md`) through the transformation engine to produce 10 fully qualified atomic step nodes (`03_Output/iirds_atomic_data.json`).

### Phase 4: Independent Quality Gate Audit
An isolated audit prompt (`02_Prompt/prompt_audit_iirds.md`), operating in a distinct LLM context without prior generation memory, performs automated verification across five safety and semantic compliance axes.

- **Audit Result:** All 10 steps achieved a confidence score of **1.0 (PASSED)** with zero safety-critical defects identified (`04_Audit/audit_result_iirds.json`).

## 4. Key Architectural Highlights

### ① Structural Formalization of Physical Safety Interlocks (STEP-006)
Narrative safety warnings—such as _"Ensure primary supply valve is closed, oil temperature is 40°C or lower, and residual pressure does not exceed 0.05 MPa"_—are structured into typed key-value pairs within the `required_physical_states` array.

When cross-referenced against live IoT/CAN-bus telemetry at runtime, this structure acts as a **deterministic hardware gate**, programmatically blocking task rendering and tool release whenever physical values violate safety envelopes.

JSON

```
"step_id": "STEP-006",
"action_type": "Depressurization",
"preconditions": {
  "required_physical_states": [
    {
      "parameter": "ValveStatus",
      "condition": "Closed",
      "sensor_type": "バルブ閉止確認"
    },
    {
      "parameter": "OilTemperature",
      "condition": "<= 40°C",
      "sensor_type": "油温センサー"
    },
    {
      "parameter": "ResidualPressure",
      "condition": "<= 0.05 MPa",
      "sensor_type": "残圧センサー"
    }
  ]
}
```

### ② Strict Role-Based Disassembly Prohibition (STEP-001)
Prohibitory warnings in manual headers are assigned explicit role constraints: `target_audience: "iirds:Operator"` with `prohibited_action: true`.

At runtime, this metadata guarantees that operator accounts encounter disabled disassembly interfaces and mandatory warning overlays, enforcing structural access separation directly from the data layer.

### ③ Automated Deprecated Component Filtering (STEP-009)
The pipeline parses manual warnings (e.g., _"Caution: Legacy cartridge FLT-X200-OLD has been discontinued and must not be used"_) and restricts replacement options to active, valid catalog numbers (`FLT-STD-01`, `FLT-X200-STD`, `FLT-X200-HD`). Superseded items are eliminated upstream from maintenance guidance.

### ④ Direct Geometric Node Anchoring (`COMP-HOUSING-01`)
Across inspection (STEP-004), cover removal (STEP-007), and torque tightening (STEP-010), the target 3D CAD identifier (`COMP-HOUSING-01`) is consistently bound to atomic tasks. This provides direct geometric anchor points for camera targeting, automated explode animations, and localized part highlighting within the Web3D viewer.

## 5. Quality Assurance and Validation Framework (5-Axis Audit)

Engineered for production enterprise DataOps, the independent quality audit systematically evaluates extraction outputs against five operational criteria:

|**Validation Axis**|**Verification Scope**|**Criticality Level**|
|---|---|---|
|**1. TargetAudience Integrity**|Verifies role boundaries between operators and technicians.|**Critical (Prevents unauthorized maintenance risks)**|
|**2. PhysicalState Precision**|Validates sensor parameters, threshold limits, and comparison operators.|**Critical (Prevents interlock bypass failures)**|
|**3. Atomic Granularity**|Guarantees single-action, single-assertion execution per step.|Medium (Avoids 3D animation concurrency conflicts)|
|**4. Prohibition Flag Coverage**|Confirms `prohibited_action: true` is asserted on all negative directives.|High (Mitigates operational safety hazards)|
|**5. Entity & Supply Mapping**|Confirms exact binding of component IDs (`COMP-HOUSING-01`) and tools (`TOOL-A`).|High (Eliminates Step C graph link failures)|

### Human-in-the-Loop Workflow Integration
In alignment with the governance model established in Step A, only atomic datasets securing a **1.0 audit score** pass automatically to Step C (Knowledge Graph Integration). Sub-threshold scores or syntax anomalies trigger immediate routing to Technical Communicator review queues, enforcing enterprise-grade information provenance.