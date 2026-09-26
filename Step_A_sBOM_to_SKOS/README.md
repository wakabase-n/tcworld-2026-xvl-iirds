# Step A: Automated Transformation of Service BOM (CSV) into a W3C SKOS Concept Scheme (JSON-LD)

## 1. Objective and Positioning: Establishing a Semantic Hub Across Disparate Data Silos

In industrial manufacturing and field service operations, textual expressions in technical documentation (e.g., _"high-dust filter element"_), engineering/service part numbers (e.g., `FLT-X200-HD`), and 3D CAD geometric node identifiers (e.g., `COMP-HOUSING-01`) are managed across isolated systems and terminology spaces.

This step takes a flat Service Bill of Materials (sBOM) in CSV format as input and automatically transforms it into a machine-actionable concept dictionary in **JSON-LD**, strictly conforming to the W3C **SKOS (Simple Knowledge Organization System)** standard.

By doing so, it establishes a foundational **"Semantic Hub"** that enables loose coupling at the identifier level between 3D geometric components and iiRDS procedural tasks in the downstream pipeline (Step C).

## 2. Directory Layout


```
Step_A_sBOM_to_SKOS/
├── 01_Input/
│   └── service_bom.csv                      # Source input: Flat sBOM in CSV format
├── 02_Prompt/
│   ├── prompt_csv_to_skos.md                # Transformation prompt with explicit ontology mapping rules
│   └── prompt_audit_skos.md                 # Independent deterministic audit prompt
├── 03_Output/
│   └── skos_concepts_sBOM.jsonld            # Artifact: Compiled SKOS Concept Scheme (JSON-LD)
├── 04_Audit/
│   └── audit_result_skos.json               # Automated audit log (Score: 1.0 PASSED)
└── README.md                                # Step documentation
```

## 3. Execution Pipeline


![](Pasted%20image%2020260926104138.png)

### Phase 1: Execution of the Mapping-Constrained Transformation Prompt

Executes the schema-guided prompt (`02_Prompt/prompt_csv_to_skos.md`), projecting each CSV attribute deterministically onto formal SKOS and iiRDS ontologies:

- `PartNumber` ➔ Unique concept entity (`skos:Concept` / IRI: `ex:Part/{PartNumber}`) and alphanumeric code (`skos:notation`)
- `PartName` ➔ Canonical preferred label (`skos:prefLabel`)
- `Notes` / `PartName` ➔ Inferred colloquialisms, acronyms, and lexical variants (`skos:altLabel`)
- `ComponentID` ➔ Broader concept pointing to the assembly/3D geometric node (`skos:broader`)
- `ApplicableVariant` ➔ Target product variant relationship (`iirds:ProductVariant`)
- `Status` ➔ Lifecycle state (`ext:lifecycleStatus`) and procurement availability flag (`ext:isAvailable: false`)

### Phase 2: Independent Quality Gate Audit

An independent validation prompt (`02_Prompt/prompt_audit_skos.md`), running in an isolated context, evaluates the generated JSON-LD across four deterministic axes: **Schema Completeness**, **Identifier Uniqueness**, **Semantic Plausibility of Inferred Synonyms**, and **Business Rule Enforcement**.

- **Audit Result:** All 4 concept nodes achieved a confidence score of **1.0 (PASSED)** (`04_Audit/audit_result_skos.json`).

## 4. Key Design Highlights

### ① Native JSON-LD Graph Representation Ready for RDF Triplestores
The output is not an arbitrary JSON payload; it is a fully qualified JSON-LD document with comprehensive `@context` and `@graph` definitions. It can be imported directly into Neo4j (via the `neosemantics` plugin) or native RDF graph stores without intermediate schema transformation or data restructuring:


```
{
  "@context": {
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "iirds": "http://iirds.tekom.de/iirds/1.0/core#",
    "ex": "http://example.com/project/"
  },
  "@graph": [
    {
      "@id": "ex:Part/FLT-X200-HD",
      "@type": "skos:Concept",
      "skos:prefLabel": "Hydraulic filter element for high-dust environments",
      "skos:altLabel": ["Opt-HD element", "Filter cartridge for high-dust environments"],
      "skos:broader": "ex:Component/COMP-HOUSING-01",
      "iirds:relates-to-product-variant": "ex:Variant/SP-X200",
      "ext:optionCode": "Opt-HD",
      "ext:isAvailable": true
    }
  ]
}
```

### ② Automated Mining of Colloquial Variants (`skos:altLabel`)
Field technicians and legacy documentation frequently employ informal terminology (e.g., _"Opt-HD cartridge"_, _"legacy element"_) rather than standardized part numbers. The pipeline mines these natural language expressions from unstructured remarks, populating `skos:altLabel` arrays. This significantly expands retrieval recall for downstream AI agents and field search engines without degrading ontological precision.

### ③ Upstream Business Rule Governance (Deprecated Part Interlocks)
For superseded or deprecated components (`Status: "Deprecated"` such as `FLT-X200-OLD`), the pipeline enforces business logic by asserting `ext:isAvailable: false`. This structural constraint guarantees that deprecated parts are deterministically blocked from procurement and assembly workflows at the data architecture layer, preventing downstream ordering errors.

## 5. Scaling to Enterprise DataOps: Three-Tier Automated Triage

While small-scale datasets can be reviewed manually, enterprise operations involving tens of thousands of catalog items require an automated, auditable ingestion pipeline.

This architecture incorporates a **Human-in-the-Loop (HITL) triage model** triggered directly by the auditor's deterministic confidence score:

![](Pasted%20image%2020260926105410.png)


- **Pass 1 (Autonomous Approval):** Score $\ge$ 0.95. Directly imported into the staging knowledge graph without human intervention (projected coverage: 80–90% of steady-state catalog ingestion).
    
- **Pass 2 (Targeted Human Triage):** Score 0.70–0.94. Ambiguities (such as unverified `altLabel` derivations or questionable classification mappings) trigger targeted review flags, routing only the suspect records to Technical Communicators.
    
- **Pass 3 (Deterministic Rejection & Self-Correction):** Score < 0.70 or critical constraint violations (e.g., missing primary keys or malformed IRIs). The payload is immediately rejected, and validation errors are fed back to the LLM agent for automated re-generation.

By operationalizing this automated quality gate, enterprises can reduce manual verification overhead by over 80% while upholding strict data integrity across the global digital thread.