
# YottaFlex Manufacturing Traceability Configuration

RANDOM_SEED = 20261022

# Required dataset quantities
NUM_PRODUCTS = 200
NUM_SUPPLIERS = 50
NUM_MATERIAL_LOTS = 2000
NUM_PRODUCTION_ORDERS = 5000
NUM_INSPECTIONS = 20000

# Output settings
OUTPUT_DIR = "data/generated"

# ID configuration
PRODUCT_PREFIX = "SKU"
ORDER_PREFIX = "WO"
DEFECT_PREFIX = "DEF"
CAPA_PREFIX = "CAPA"
# Machine and Process Step configuration
NUM_MACHINES = 25
NUM_PROCESS_STEPS = 15000

MACHINE_PREFIX = "MCH"
PROCESS_STEP_PREFIX = "STEP"