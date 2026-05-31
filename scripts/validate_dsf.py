import os
import sys

def validate_dsf(dsf_txt_path, release_path):
    print(f"Validating resources for {dsf_txt_path} in {release_path}...")
    
    if not os.path.exists(dsf_txt_path):
        print(f"Error: DSF text file not found: {dsf_txt_path}")
        return False
        
    resources = []
    with open(dsf_txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('OBJECT_DEF') or line.startswith('POLYGON_DEF'):
                parts = line.split()
                if len(parts) >= 2:
                    resources.append(parts[1])
    
    missing_count = 0
    for res in resources:
        # X-Plane paths in DSF are usually relative to the scenery root
        # e.g., objects\ts_lavra_belltower.obj
        full_path = os.path.join(release_path, res)
        if not os.path.exists(full_path):
            print(f"MISSING RESOURCE: {res}")
            print(f"  Expected at: {full_path}")
            missing_count += 1
            
    if missing_count == 0:
        print(f"Success: All {len(resources)} resources found.")
        return True
    else:
        print(f"Validation failed: {missing_count} resources missing.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_dsf.py <dsf_txt_path> <release_path>")
        sys.exit(1)
        
    dsf_path = sys.argv[1]
    rel_path = sys.argv[2]
    
    if not validate_dsf(dsf_path, rel_path):
        sys.exit(1)
