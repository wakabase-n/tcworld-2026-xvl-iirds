# Step D: Neo4j Graph Database Deployment and Infrastructure Setup

## 1. Objective and Architectural Rationale: Why a Graph Database Over Flat JSON Payloads?

The unified dataset generated in Step C (`PoC_manual_AtomicData.json`) formalizes the semantic relationships connecting 3D CAD geometric node identifiers (XVL), atomic procedural steps (iiRDS), and replacement catalog parts (SKOS).

However, deploying this data model as an active runtime governance engine for field devices and autonomous agents exposes clear computational limits when relying on static, flat JSON files.

Neo4j was selected as the operational graph database for three primary reasons:

1. **Deterministic Multi-Hop Traversal at Constant Time**
    Evaluating relational dependencies across multiple boundaries—such as resolving an `AtomicStep` through an assembly `Part`, down to its target product `Variant`, and filtering by an optional equipment code (`optionCode`)—requires multi-pass iterative parsing in JSON. In a native graph database, these paths are traversed directly via physical memory pointers, executing multi-hop queries deterministically within single-digit milliseconds.
    
2. **Unified Topology Coupling Schema (TBox) and Instance (ABox) Layers**
    Formal ontology definitions from international standards (iiRDS Core, Machinery, and W3C SKOS) are instantiated alongside operational maintenance records within a shared graph space. This grounds procedural assertions directly in standardized classification hierarchies.
    
3. **Sub-Graph Extraction for GraphRAG Context Injection**
    Instead of appending entire narrative manuals into large-language model (LLM) context windows, Cypher queries extract tightly bounded sub-graphs scoped to the operator's entitlement role, current machine fault codes, and immediate component targets. This provides deterministic boundaries for Graph-Augmented Generation (GraphRAG).

## 2. Structural Differentiation: Native Graph Storage vs. Relational (RDBMS) Models

Representing cyber-physical relationships in technical documentation requires moving away from tabular relational architectures toward native graph storage.

<img width="1606" height="825" alt="image" src="https://github.com/user-attachments/assets/e5d8a33e-2a0b-4b51-a433-1fc6fe96825e" />

### ① Multi-Table JOIN Latency vs. Index-Free Adjacency
- **Relational Databases (RDBMS):**
    Data is persisted across row-and-column tables. Traversing relationships requires looking up foreign keys across intermediate junction tables and querying indexes repeatedly. As multi-hop traversal depth increases, computational overhead and join complexity scale exponentially.
    
- **Native Graph Databases (Index-Free Adjacency):**
    Every node acts as a pointer cluster, directly referencing adjacent nodes via physical memory offsets. Traversal executes without global index lookups, ensuring evaluation time is governed exclusively by the size of the visited sub-graph rather than total database scale.

### ② Structural Characteristic Comparison

|**Dimension**|**Relational Databases (RDBMS)**|**Native Graph Databases (Graph DB)**|
|---|---|---|
|**Data Representation**|Rigid tabular schemas (rows/columns)|Flexible nodes, typed relationships, properties|
|**Relationship Handling**|Inferred indirectly through foreign key indexes|First-class entities via direct pointer traversal|
|**Multi-Hop Traversal**|High latency; quadratic computational growth|Single-millisecond; proportional only to path length|
|**Schema Evolution**|Costly migrations, schema locks, DDL refactoring|Non-destructive; adding an edge does not disrupt nodes|
|**Primary Domain**|Homogeneous transactional processing (ERP, billing)|Complex, multi-modal knowledge integration & governance|

### ③ Non-Destructive Schema Extension for Industrial Data
In an RDBMS, unifying maintenance instructions, 3D CAD coordinate identifiers, and operational telemetry thresholds into a single schema forces widespread denormalization or dense junction table hierarchies.

In a native property graph, new relations (such as attaching physical sensor interlocks to existing procedural nodes) are layered non-destructively without altering existing entity definitions or breaking upstream consumers.

## 3. Directory Layout

Plaintext

```
Step_D_Graph_Engine_Setup/
├── 01_Input/
│   └── PoC_manual_AtomicData.json           # Step C Artifact: Compiled knowledge graph payload
├── 02_TBox_Setup/
│   └── n10s_init_and_import_vocab.cypher    # neosemantics setup & iiRDS/SKOS ontology import
├── 03_ABox_Import/
│   ├── import_atomic_data.py                # ABox data loader (Python / Official Neo4j Driver)
│   └── import_atomic_data.cypher            # ABox data loader (Cypher / APOC implementation)
├── 04_Verification/
│   └── verify_graph_structure.cypher        # Structural integrity and traversal verification
└── README.md                                # Step documentation
```

## 4. Deployment Pipeline (2-Phase Architecture)

<img width="1158" height="917" alt="image" src="https://github.com/user-attachments/assets/ce3a9559-0390-47f5-9d85-c201f21500b9" />


### Phase 1: Deploying the Standard Ontology Layer (TBox)
Initializes the **neosemantics (n10s)** plugin on a Neo4j 5.x instance to import official iiRDS specifications (`iirds-core.rdf`, `iirds-machinery.rdf`) and the W3C SKOS vocabulary (`02_TBox_Setup/n10s_init_and_import_vocab.cypher`).

- **Ontological Baseline:** Establishes **380 class/property nodes and 532 hierarchical relationships** directly within the database graph schema.
- This provides formal taxonomy definitions (e.g., verifying that `iirds:Operator` and `iirds:ServiceTechnician` derive from common role superclasses).
    

### Phase 2: Ingesting Operational Instance Data (ABox)
Parses the Step C output payload (`PoC_manual_AtomicData.json`) and projects it into the graph using `03_ABox_Import/import_atomic_data.py` (or `import_atomic_data.cypher`).

- **Instantiated Topological Entities:**
    - Procedural Execution Nodes (`:AtomicStep`): 10 records (`STEP-001` through `STEP-010`)
    - 3D Geometry Bindings (`:TARGETS_COMPONENT`): 5 edges terminating on `COMP-HOUSING-01`
    - Resource & Tooling Edges (`:REQUIRES_SUPPLY`): 7 associations (specialty tools, PPE, filter elements)
    - Physical Interlock Rules (`:REQUIRES_PHYSICAL_STATE`): 3 sensor gate nodes (Valve Status, Fluid Temp, Line Pressure)
- The compiled ABox procedures attach directly to the formal TBox schema, yielding an integrated, standard-compliant knowledge graph.

## 5. Graph Structural Verification

Following data ingestion, run the verification suite (`04_Verification/verify_graph_structure.cypher`) in the Neo4j Browser or `cypher-shell` to validate topological continuity.

### Verifying End-to-End Node Linkage (Step ➔ 3D Component ➔ Physical State)

Cypher

```
MATCH (s:AtomicStep)
OPTIONAL MATCH (s)-[r1:TARGETS_COMPONENT]->(c)
OPTIONAL MATCH (s)-[r2:REQUIRES_PHYSICAL_STATE]->(ps)
RETURN s.id AS step_id, s.description AS description, c.component_id AS target_3d, ps.parameter AS physical_param
ORDER BY s.id;
```

### Validating Complex Interlock Constraints (STEP-006)

Cypher

```
MATCH (s:AtomicStep {id: 'STEP-006'})-[:REQUIRES_PHYSICAL_STATE]->(ps)
RETURN s.id AS step_id, ps.parameter AS parameter, ps.condition AS condition, ps.sensor_type AS sensor_type;
```

## 6. Target Milestone and Readiness

Completion of this stage establishes:

- **An active iiRDS/SKOS ontological substrate** consisting of 380 concepts and 532 semantic links.
- **Persistent instance links** binding 10 atomic maintenance procedures to 3D geometry anchors and physical sensor conditions.
- **A production-ready graph interface** supporting high-frequency Bolt protocol evaluations from edge runtimes.

The knowledge graph is now fully prepared to evaluate incoming sensor states and UI interactions.

Proceed to **Step E: Runtime Governance Validation** to review deterministic M2M batch execution logs (Step E-1) and interactive Google Notebook conversational verification (Step E-2).

---

### 📜 License & Intellectual Property Notice
All inputs, prompt templates, generated outputs, and audit artifacts within this directory (`Step_D_Graph_Engine_Setup/`) are authored by Natsuki Wakabayashi and licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

Copyright (c) 2026 Natsuki Wakabayashi/ISE.
