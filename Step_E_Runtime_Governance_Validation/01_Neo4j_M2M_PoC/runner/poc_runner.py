import json
import os
import subprocess
from neo4j import GraphDatabase

def get_host_ip():
    if os.getenv("NEO4J_HOST"):
        return os.getenv("NEO4J_HOST")
    try:
        host_ip = subprocess.check_output(
            "ip route | grep default | awk '{print $3}'", 
            shell=True
        ).decode().strip()
        if host_ip:
            return host_ip
    except Exception:
        pass
    return "localhost"

HOST_IP = get_host_ip()
NEO4J_URI = os.getenv("NEO4J_URI", f"bolt://{HOST_IP}:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")  # Configured database password

def run_poc():
    # 1. Ingest 3-stream runtime input parameters
    with open('sensor_state.json', 'r', encoding='utf-8') as f:
        sensor = json.load(f)
    with open('ui_event.json', 'r', encoding='utf-8') as f:
        ui = json.load(f)
    with open('user_profile.json', 'r', encoding='utf-8') as f:
        user = json.load(f)

    step_id = ui.get("current_step_id", "STEP-007")
    user_role = user.get("user_profile", "iirds:Operator")
    pressure = sensor.get("hydraulic_pressure_mpa", 0.0)

    # 2. Cypher query to traverse the iiRDS / AtomicData graph substrate
    # Evaluates prerequisite task constraints (STEP-006 residual pressure) and role entitlements (targetAudience)
    cypher_query = """
    MATCH (s:Resource {uri: $step_id})
    OPTIONAL MATCH (s)-[:targets_component]->(comp:Resource)
    
    // Retrieve preceding depressurization task (STEP-006) and linked physical constraints
    OPTIONAL MATCH (depress_step:Resource {uri: 'STEP-006'})-[:hasPhysicalState]->(cond:Resource)
    WHERE cond.parameter = 'ResidualPressure'

    // Deterministic evaluation logic (Executed entirely within Cypher)
    WITH s, comp, cond,
         // 1. Role entitlement check
         (s.targetAudience = $user_role OR s.targetAudience = 'iirds:Operator') AS role_ok,
         // 2. Residual pressure safety gate (<= 0.05 MPa)
         ($pressure <= 0.05) AS pressure_safe

    WITH s, comp, role_ok, pressure_safe,
         (role_ok AND pressure_safe) AS permitted

    RETURN {
      interlock_status: {
        permitted: permitted,
        warning_level: CASE 
          WHEN NOT role_ok THEN 'CRITICAL'
          WHEN NOT pressure_safe THEN 'WARNING'
          ELSE 'NONE'
        END,
        reason_code: CASE 
          WHEN NOT role_ok THEN 'ERR_UNAUTHORIZED_ROLE'
          WHEN NOT pressure_safe THEN 'ERR_PRESSURE_REMAINING'
          ELSE 'SUCCESS'
        END
      },
      hmi_action: {
        target_part_id: coalesce(comp.componentId, 'COMP-HOUSING-01'),
        highlight_mode: CASE 
          WHEN NOT permitted THEN 'BLINK_RED' 
          ELSE 'HIGHLIGHT_GREEN' 
        END,
        camera_action: CASE 
          WHEN NOT permitted THEN 'ZOOM_TO_PART' 
          ELSE 'KEEP' 
        END
      },
      guidance_content: {
        message_text: CASE 
          WHEN NOT role_ok THEN 'ERROR: Unauthorized operation. Machine operators are prohibited from disassembling this component.'
          WHEN NOT pressure_safe THEN 'WARNING: Residual circuit pressure detected (' + toString($pressure) + ' MPa). Execute depressurization procedure STEP-006 before proceeding.'
          ELSE 'Safety verification cleared: ' + s.prefLabel
        END,
        next_step_id: CASE WHEN permitted THEN 'STEP-008' ELSE null END
      }
    } AS output_json
    """

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run(
            cypher_query, 
            step_id=step_id, 
            user_role=user_role, 
            pressure=pressure
        )
        record = result.single()
        driver.close()

    if not record or not record["output_json"]:
        print("[ERROR] Failed to retrieve traversal result from graph query.")
        return

    output_data = record["output_json"]

    # 3. Persist Output JSON response
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("=== PoC Execution Completed ===")
    print(f"Target Step : {step_id}")
    print(f"Permitted   : {output_data['interlock_status']['permitted']}")
    print(f"Reason Code : {output_data['interlock_status']['reason_code']}")
    print(f"Message     : {output_data['guidance_content']['message_text']}")
    print(f"Output File : output.json")

if __name__ == "__main__":
    run_poc()