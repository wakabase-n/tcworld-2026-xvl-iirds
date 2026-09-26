// ==========================================
// 1. Prerequisites & neosemantics (n10s) Configuration
// ==========================================

// Create uniqueness constraint on Resource URI (Mandatory prerequisite for n10s)
CREATE CONSTRAINT n10s_unique_resources IF NOT EXISTS
FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

// Initialize graph configuration (Shorten URI prefixes and map RDF types to native labels)
CALL n10s.graphconfig.init({
  handleVocabUris: "SHORTEN",
  handleRDFTypes: "LABELS",
  keepLangTag: false
});

// Define core namespace prefix mappings
CALL n10s.nsmapper.add("iirds", "http://iirds.tekom.de/iirds/1.0/core#");
CALL n10s.nsmapper.add("skos", "http://www.w3.org/2004/02/skos/core#");
CALL n10s.nsmapper.add("rdfs", "http://www.w3.org/2000/01/rdf-schema#");

// ==========================================
// 2. Ingest W3C SKOS Vocabulary (TBox Schema)
// ==========================================

CALL n10s.rdf.import.fetch(
  "http://www.w3.org/2004/02/skos/core",
  "RDF/XML"
);

// ==========================================
// 3. Ingest Official iiRDS Vocabularies (Core & Machinery)
// Note: Place source RDF files into the Neo4j server 'import' directory prior to execution
// ==========================================

CALL n10s.rdf.import.fetch(
  "file:///iirds-core.rdf",
  "RDF/XML"
);

CALL n10s.rdf.import.fetch(
  "file:///iirds-machinery.rdf",
  "RDF/XML"
);