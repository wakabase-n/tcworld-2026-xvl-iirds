// =============================================================================
// verify_graph_structure.cypher
// Objective: Structural and operational sanity verification of the knowledge graph
//            post-ingestion, verifying schema and runtime traversal pathways.
// =============================================================================

// -----------------------------------------------------------------------------
// 1. Schema Layer (TBox) Verification
// -----------------------------------------------------------------------------

// Verify iiRDS and SKOS ontology class nodes (Sample top 20)
MATCH (c:Resource)
WHERE c.uri STARTS WITH "http://iirds.tekom.de/iirds/" 
   OR c.uri STARTS WITH "http://www.w3.org/2004/02/skos/"
RETURN labels(c) AS Labels, c.uri AS URI, c.rdfs__label AS Label
LIMIT 20;

// Verify TargetAudience class inheritance hierarchy (rdfs:subClassOf)
MATCH (sub:Resource)-[:rdfs__subClassOf]->(parent:Resource)
WHERE parent.uri CONTAINS "TargetAudience"
RETURN sub.uri AS SubClass, parent.uri AS ParentClass;


// -----------------------------------------------------------------------------
// 2. Instance Data Layer (ABox) Structural & Topological Verification
// -----------------------------------------------------------------------------

// Visualize global connectivity: Atomic steps to 3D components, parts, and physical states
MATCH (s:AtomicStep)
OPTIONAL MATCH (s)-[r1:TARGETS]->(c:Component)
OPTIONAL MATCH (s)-[r2:REQUIRES_PART]->(p:Part)
OPTIONAL MATCH (s)-[r3:REQUIRES_STATE]->(ps:PhysicalState)
RETURN s, r1, c, r2, p, r3, ps
LIMIT 25;

// Pinpoint verification of physical safety interlocks and supplies on STEP-006
MATCH (s:AtomicStep {step_id: "STEP-006"})-[:REQUIRES_STATE]->(ps:PhysicalState)
MATCH (s)-[:REQUIRES_SUPPLY]->(sup:Supply)
RETURN s.step_id AS StepID,
       s.description AS ActionDescription,
       collect(DISTINCT ps.sensor_type + ": " + ps.parameter + " " + ps.condition) AS SafetyInterlocks,
       collect(DISTINCT sup.name) AS RequiredSupplies;


// -----------------------------------------------------------------------------
// 3. Runtime Governance Queries (Deterministic Traversal Verification)
// -----------------------------------------------------------------------------

// ① Role-Based Entitlement: Retrieve operator procedures and safety prohibitions
MATCH (s:AtomicStep)
WHERE s.target_audience = "iirds:Operator"
OPTIONAL MATCH (s)-[:TARGETS]->(c:Component)
RETURN s.step_id AS StepID,
       s.description AS Description,
       s.prohibited_action AS IsProhibited,
       c.component_id AS Target3DNode
ORDER BY s.step_id;

// ② Variant & Option Compatibility: Resolve element for SP-X200 with Opt-HD specification
MATCH (s:AtomicStep {step_id: "STEP-009"})-[:REQUIRES_PART]->(p:Part)
WHERE p.applicable_variant = "ex:Variant/SP-X200"
  AND (p.option_code = "Opt-HD" OR p.option_code IS NULL)
RETURN s.step_id AS StepID,
       p.part_number AS PartNumber,
       p.pref_label AS Label,
       p.option_code AS OptionCode;