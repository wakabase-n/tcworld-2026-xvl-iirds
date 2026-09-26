# Step C: Multi-Modal Semantic Binding (3D XVL ✕ iiRDS) via SKOS Concept Scheme Hub

## 1. Objective and Positioning: Decoupled Multi-Modal Integration via a Semantic Hub

In discrete manufacturing and plant maintenance, 3D CAD/geometric structures (e.g., XVL) and procedural documentation (e.g., iiRDS) are governed by distinct lifecycles, data architectures, and nomenclature systems.

Hard-coding associations directly between procedural text and CAD component trees creates rigid dependencies: any revision to the 3D model geometry or change in technical manual wording breaks downstream execution logic.

This step utilizes the **SKOS Concept Scheme** created in Step A as an intermediary **"Semantic Hub."** It establishes a standoff, non-destructive binding between the **iiRDS atomic steps** extracted in Step B and the **3D geometric node identifier (`COMP-HOUSING-01`)**.

This standoff integration links procedural knowledge with 3D spatial definitions without mutating original CAD assemblies or source documentation, yielding an integrated, bidirectional knowledge graph.

## 2. Directory Layout

Plaintext

```
Step_C_Integration_Binding/
├── 01_Input/
│   ├── skos_concepts_sBOM.jsonld            # Step A Artifact: SKOS Concept Scheme (JSON-LD)
│   └── iirds_atomic_data.json               # Step B Artifact: iiRDS Atomic Step Records (JSON)
├── 02_Prompt/
│   ├── prompt_integration_binding.md        # Multi-modal semantic binding prompt
│   └── prompt_audit_binding.md              # Independent referential integrity audit prompt
├── 03_Output/
│   └── PoC_manual_AtomicData.json           # Artifact: Unified Knowledge Graph Dataset (10 Steps)
├── 04_Audit/
│   └── audit_result_binding.json            # Quality gate audit report (Score: 1.0 PASSED)
└── README.md                                # Step documentation
```

## 3. Execution Pipeline

<img width="1027" height="912" alt="image" src="https://github.com/user-attachments/assets/302d5663-50be-45bc-afe7-b7dac668f2dc" />

### Phase 1: Execution of the Semantic Integration Prompt
Processes the SKOS scheme and iiRDS atomic step records through the integration prompt (`02_Prompt/prompt_integration_binding.md`) using strict mapping rules:

- **3D Geometric Node Anchoring**:
    Maps the procedural component reference in Step B (`target_component: "COMP-HOUSING-01"`) through the SKOS broader concept relationship (`skos:broader: "ex:Component/COMP-HOUSING-01"`), assigning it to the formal `3d_node_binding` attribute.
- **Entity Resolution**:
    Reconciles plain-text part numbers (e.g., `FLT-X200-HD`) against the SKOS dictionary, promoting them to fully qualified concept IRIs (`ex:Part/FLT-X200-HD`) and attaching variant compatibility (`ProductVariant`) and option code (`optionCode`) properties.
- **Artifact Generation**:
    Generates the unified graph payload (`03_Output/PoC_manual_AtomicData.json`), compiling execution order, physical interlocks (`PhysicalState`), 3D viewport hooks, and variant-compatible replacement parts across all 10 procedural steps.

### Phase 2: Independent Referential Integrity Audit
An isolated audit agent (`02_Prompt/prompt_audit_binding.md`) examines the generated dataset for dangling pointers, orphaned nodes, and incorrect part bindings.

- **Audit Outcome**: The dataset achieved an evaluation score of **1.0 (PASSED)** (`04_Audit/audit_result_binding.json`).
    - Broken References: **0** (All referenced IRIs resolve within the ontology or dataset)
    - 3D Node Bindings: **5 out of 5 exact structural matches**
    - SKOS Entity Resolution: **3 out of 3 part numbers correctly mapped**

## 4. Key Architectural Highlights

### ① Elevating Raw Strings to Computable Semantic IRIs
In STEP-009 (Filter Element Replacement), arbitrary text strings are resolved into dereferenceable RDF concepts via the SKOS scheme:

JSON

```
{
  "supply_type": "Component",
  "skos_concept_iri": "ex:Part/FLT-X200-HD",
  "pref_label": "Hydraulic filter element for high-dust environments",
  "part_number": "FLT-X200-HD",
  "applicable_variant": "ex:Variant/SP-X200",
  "option_code": "Opt-HD",
  "lifecycle_status": "Active"
}
```

When an edge application provides machine context (e.g., _"Model: SP-X200 with Heavy-Duty Option Opt-HD"_), the runtime traversal engine resolves the exact component (`FLT-X200-HD`) and its maintenance constraints in a single path evaluation, eliminating client-side filtering logic.

### ② Convergent Geometric Multiplexing on `COMP-HOUSING-01`
Five distinct procedural tasks converge on the single geometric identifier `COMP-HOUSING-01`:

- Unauthorized Disassembly Prohibition Warning (STEP-001)
- External Visual Leak Inspection (STEP-004)
- Housing Cover Removal (STEP-007)
- Replacement Cartridge Insertion (STEP-009)
- Housing Cover Torque Tightening (STEP-010)

Because these tasks share a common geometric anchor, the Web3D runtime supports bidirectional interactions: clicking the housing component in the viewport retrieves all linked procedural lifecycle states, and advancing procedural steps triggers corresponding 3D actions (such as focus camera framing or disassembly animations).

### ③ Non-Destructive Fallback for Non-sBOM Entities (Tooling & PPE)
Specialty tools (`TOOL-A`) and personal protective equipment in STEP-006 originate from operational safety procedures rather than the engineering BOM, and therefore lack entries in the SKOS part catalog.

Rather than generating speculative concepts, the pipeline assigns `skos_concept_iri: null` while preserving local properties (`part_number: "TOOL-A"`, `supply_type: "Tool"`). This prevents graph corruption while retaining necessary tooling constraints for runtime verification.

## 5. Topological Graph Structure

The completion of Step C links four functional layers into a continuous digital thread:

<img width="1526" height="835" alt="image" src="https://github.com/user-attachments/assets/4a93a7c7-e59d-401a-8c7b-3f46525e9102" />

## 6. Summary of Knowledge Pipeline & Foundation (Steps A–C)

Steps A through C complete the compilation pipeline, converting siloed technical data into an integrated knowledge graph:

|**Stage**|**Input ➔ Output Target**|**Architectural Function**|**Audit Validation**|
|---|---|---|---|
|**Step A**|sBOM CSV ➔ SKOS JSON-LD|Lexical normalization; establishes broader 3D anchors|**Score: 1.0 (PASSED)**|
|**Step B**|Narrative Manual ➔ iiRDS JSON|Atomic step decomposition; physical state extraction|**Score: 1.0 (PASSED)**|
|**Step C**|Multi-Modal 3D ✕ iiRDS Binding|Synchronizes 3D spatial, procedural, and BOM layers|**Score: 1.0 (PASSED)**|

Every phase achieved a verified audit score of **1.0**, establishing a validated dataset (`PoC_manual_AtomicData.json`).

In **Step D (Neo4j Graph Database Deployment)**, this dataset is ingested alongside formal iiRDS and SKOS ontologies to configure the real-time graph traversal engine.

