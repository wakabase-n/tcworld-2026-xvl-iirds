// =============================================================================
// import_atomic_data.cypher
// Objective: Ingest PoC_manual_AtomicData.json to batch-create Neo4j nodes and edges
// Prerequisites:
//   - APOC plugin is installed and enabled
//   - PoC_manual_AtomicData.json is placed inside the Neo4j 'import' directory
// =============================================================================

// 1. Create Uniqueness Constraints (Indexes)
CREATE CONSTRAINT FOR (s:AtomicStep) REQUIRE s.step_id IS UNIQUE;
CREATE CONSTRAINT FOR (c:Component) REQUIRE c.component_id IS UNIQUE;
CREATE CONSTRAINT FOR (p:Part) REQUIRE p.part_number IS UNIQUE;

// 2. Load JSON Payload and Unwind Graph Structure
CALL apoc.load.json("file:///PoC_manual_AtomicData.json") YIELD value
UNWIND value.knowledge_graph AS step

// --- (1) Instantiate AtomicStep Nodes ---
MERGE (s:AtomicStep {step_id: step.step_id})
SET s.chapter = step.chapter,
    s.target_audience = step.target_audience,
    s.action_type = step.action_type,
    s.description = step.description,
    s.prohibited_action = step.prohibited_action

// --- (2) Bind 3D Geometric Component Nodes ---
FOREACH (_ IN CASE WHEN step.3d_node_binding IS NOT NULL THEN [1] ELSE [] END |
  MERGE (c:Component {component_id: step.3d_node_binding.component_id})
  SET c.iri = step.3d_node_binding.iri
  MERGE (s)-[:TARGETS]->(c)
)

// --- (3) Bind Physical Safety Interlock States (Preconditions) ---
FOREACH (ps IN step.preconditions.required_physical_states |
  MERGE (pstate:PhysicalState {
    parameter: ps.parameter,
    condition: ps.condition
  })
  SET pstate.sensor_type = ps.sensor_type
  MERGE (s)-[:REQUIRES_STATE]->(pstate)
)

// --- (4) Bind SKOS Parts and Operational Supplies (Tooling / PPE) ---
FOREACH (supply IN step.bound_supplies |
  // Component Items Resolved to SKOS Concepts
  FOREACH (_ IN CASE WHEN supply.supply_type = "Component" THEN [1] ELSE [] END |
    MERGE (part:Part {part_number: supply.part_number})
    SET part.skos_concept_iri = supply.skos_concept_iri,
        part.pref_label = supply.pref_label,
        part.applicable_variant = supply.applicable_variant,
        part.option_code = supply.option_code,
        part.lifecycle_status = supply.lifecycle_status
    MERGE (s)-[:REQUIRES_PART]->(part)
  )
  // Tooling and Personal Protective Equipment (Non-BOM Supplies)
  FOREACH (_ IN CASE WHEN supply.supply_type <> "Component" THEN [1] ELSE [] END |
    MERGE (sup:Supply {name: supply.pref_label})
    SET sup.supply_type = supply.supply_type,
        sup.part_number = supply.part_number
    MERGE (s)-[:REQUIRES_SUPPLY]->(sup)
  )
);