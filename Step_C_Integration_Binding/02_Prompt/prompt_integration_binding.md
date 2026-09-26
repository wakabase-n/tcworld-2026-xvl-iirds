
# Role
You are an expert in Knowledge Graph Engineering, Semantic Data Integration, and ontology-driven technical communication architectures.

# Task
Read the two attached datasets (the SKOS Concept Scheme and the iiRDS Atomic Step records) and generate a unified knowledge graph dataset serialized in JSON format. Use the SKOS concept scheme as a central semantic hub to establish complete, bidirectional standoff bindings between 3D geometric node identifiers (XVL) and iiRDS procedural tasks.

# Input Files
1. SKOS Concept Scheme (sBOM): `skos_concepts_sBOM.jsonld`
2. iiRDS Atomic Step Dataset: `iirds_atomic_data.json`

# Binding & Entity Resolution Rules

1. **3D Geometric Node Binding:**
   - Map each `target_component` identifier declared in the Step B atomic steps (e.g., `COMP-HOUSING-01`) directly to the corresponding `skos:broader` parent concept node (`ex:Component/COMP-HOUSING-01`) defined in the SKOS scheme, outputting a qualified `3d_node_binding` object.

2. **Entity Resolution for Parts and Supplies:**
   - Cross-reference part numbers (`part_number`) and names (`name`) in `required_supplies` from Step B against the `skos:notation`, `skos:prefLabel`, and `skos:altLabel` lexical properties in the SKOS scheme.
   - Upon positive resolution, elevate raw string literals into formal, dereferenceable concept IRIs (e.g., `ex:Part/FLT-X200-HD`).
   - Attach all associated ontological metadata from the SKOS scheme (`iirds:ProductVariant`, `ext:optionCode`, `ext:lifecycleStatus`) directly to the bound supply object.
   - If an item does not originate from the catalog BOM (such as generic specialty tooling or PPE), preserve its local attributes while safely setting `skos_concept_iri: null` (non-destructive fallback).

3. **Graph Topology Structuring:**
   - Structure each node around a primary `step_id` key, explicitly articulating directional relationships connecting `target_audience`, `action_type`, `preconditions` (`required_physical_states`), and `bound_supplies`.

# Output JSON Schema Structure

Adhere strictly to the following integrated Knowledge Graph schema:

```json
{
  "graph_metadata": {
    "document_id": "MAN-HYD-2026-01",
    "concept_scheme": "ex:Scheme/sBOM-Hydraulics",
    "binding_status": "SUCCESS"
  },
  "knowledge_graph": [
    {
      "step_id": "STEP-009",
      "chapter": "Chapter 2: Hydraulic Filter Element Inspection & Replacement (For Service Engineers)",
      "target_audience": "iirds:Operator | iirds:ServiceTechnician",
      "action_type": "Replacement",
      "description": "Specific instruction text isolated for this atomic node",
      "prohibited_action": false,
      "3d_node_binding": {
        "component_id": "COMP-HOUSING-01",
        "iri": "ex:Component/COMP-HOUSING-01"
      },
      "preconditions": {
        "required_physical_states": [
          {
            "parameter": "OilTemperature",
            "condition": "<= 40°C",
            "sensor_type": "Hydraulic oil temperature sensor"
          }
        ],
        "prerequisite_tasks": ["Close primary hydraulic fluid supply valve completely"]
      },
      "bound_supplies": [
        {
          "supply_type": "Component",
          "skos_concept_iri": "ex:Part/FLT-X200-HD",
          "pref_label": "Heavy-Duty Hydraulic Filter Element",
          "part_number": "FLT-X200-HD",
          "applicable_variant": "ex:Variant/SP-X200",
          "option_code": "Opt-HD",
          "lifecycle_status": "Active"
        }
      ]
    }
  ]
}
````

# Output Format

Output ONLY the raw, validated JSON code block (`json ...` ). Do not include any introductory text, conversational remarks, or markdown framing outside the code block.