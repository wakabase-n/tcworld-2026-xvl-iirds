
# Role
You are an expert in the iiRDS (intelligent information Request and Delivery Standard) and knowledge graph data modeling for technical communication.

# Task
Read the attached technical manual source (`MAN-HYD-2026-01.md`) and generate structured atomic step records in strict JSON format conforming to the iiRDS standard.

# Structuring & Extraction Rules

1. **Atomic Step Decomposition:**
   - Decompose procedural text and behavioral instructions into minimum execution units (Atomic Steps), where each node represents exactly "one action or one decision."

2. **TargetAudience Determination:**
   - Explicitly classify each step and section according to its intended audience persona using formal iiRDS vocabulary:
   - Examples: `iirds:Operator`, `iirds:ServiceTechnician`.

3. **PhysicalState Extraction (Lifted Metadata):**
   - Identify physical safety interlock conditions that must be satisfied before task execution (e.g., valve positions, temperature limits, residual pressure thresholds) and extract them as structured, typed attributes.

4. **Component & Tooling Entity Extraction:**
   - Detect and preserve referenced 3D component identifiers (e.g., `COMP-HOUSING-01`), catalog part numbers (e.g., `FLT-X200-HD`), and specialty tools (e.g., `TOOL-A`).

# Output JSON Schema Structure

Adhere strictly to the following JSON schema:

```json
{
  "document_id": "MAN-HYD-2026-01",
  "atomic_steps": [
    {
      "step_id": "Unique step ID (e.g., STEP-001)",
      "chapter": "Chapter / section title",
      "target_audience": "Formal iiRDS concept IRI (e.g., iirds:Operator or iirds:ServiceTechnician)",
      "action_type": "Formal action category (e.g., Inspection, Contact, SafetyCheck, Disassembly, Replacement, Operation, Depressurization, Disposal, Tightening)",
      "description": "Specific instruction text isolated for this atomic node",
      "prohibited_action": true, // Boolean: true if the step denotes a safety prohibition or hazard warning
      "target_component": "Target 3D geometric node ID (e.g., COMP-HOUSING-01, or null)",
      "preconditions": {
        "required_physical_states": [
          {
            "parameter": "Physical parameter name (e.g., ValveStatus, OilTemperature, ResidualPressure)",
            "condition": "Evaluation expression (e.g., Closed, <= 40°C, <= 0.05 MPa)",
            "sensor_type": "Telemetry source or verification sensor"
          }
        ],
        "prerequisite_tasks": ["Prerequisite human tasks (e.g., Primary supply valve closure)"]
      },
      "required_supplies": [
        {
          "supply_type": "Formal iiRDS supply category (e.g., Tool, PPE, Component)",
          "name": "Designation of equipment, tool, or PPE",
          "part_number": "Catalog part number (e.g., TOOL-A, or null)"
        }
      ],
      "applicable_variants": ["Array of applicable product variant IRIs (e.g., ex:Variant/SP-X100, ex:Variant/SP-X200)"]
    }
  ]
}
````

# Input File

Target document: `MAN-HYD-2026-01.md`

# Output Format

Output ONLY the raw, validated JSON code block (`json ...` ). Do not include any conversational preamble, commentary, or markdown framing outside the code block.