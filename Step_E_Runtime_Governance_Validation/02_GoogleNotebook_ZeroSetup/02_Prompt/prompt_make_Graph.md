# Instructions
Extract and construct deterministic Subject-Predicate-Object (SPO) triple structures grounded in iiRDS and domain-extension ontologies from the ingested atomic data payload (JSON array).

# Controlled Predicate Vocabulary
Assert ONLY the following predefined properties as the "predicate". Under no circumstances should you fabricate or invent arbitrary predicates outside this whitelist:
- `iirds:has-tool`: Tools and equipment required for task execution.
- `iirds:has-supply`: Parts, consumables, and PPE required for task execution.
- `iirds:relates-to-product-variant`: Applicable target product model or variant classification.
- `iirds:targets-component`: Target 3D geometric CAD component or physical assembly unit.
- `ex:hasPhysicalState`: Prerequisite physical conditions and telemetry interlocks (sensor states).
- `ex:hasAttribute`: Entity specifications and physical parameters (dimensions, torque ratings, option codes).
- `ex:isProhibited`: Deterministic safety prohibition flag (boolean literal: true/false).

# Extraction and Mapping Constraints
1. **Subject**:
   - As a baseline rule, use the atomic step identifier (`step_id`, e.g., "STEP-001") or the component/supply IRI as the Subject key.
2. **Object**:
   - Assign the associated target node identifier (IRI or catalog part number), or a concrete literal value (e.g., string/numeric values such as "5mm", "50 N·m").
3. **Attribute Chaining (`ex:hasAttribute`)**:
   - When detailed specifications (dimensions, engineering ratings) are associated with tooling or supplies, instantiate that tool or part identifier as the Subject and project the attribute value as the Object.

# Output Serialization Format (JSON Triples)
Output ONLY the following JSON array structure. Do not include any introductory remarks, explanations, or conversational markdown outside the code block.

```json
[
  {
    "subject_id": "STEP-001",
    "subject_label": "1. Housing Removal",
    "predicate": "iirds:has-tool",
    "object_id": "TOOL-HEX-05",
    "object_label": "Hex Wrench"
  },
  {
    "subject_id": "TOOL-HEX-05",
    "subject_label": "Hex Wrench",
    "predicate": "ex:hasAttribute",
    "object_id": null,
    "object_label": "5mm"
  }
]
