from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider

"""
THIS IS NOT A REAL CLIENT,
BUT IT SIMULATES THE DATA THAT COMES FROM THE GLUCOSE PROVIDER WHEN A
PUBLISHER ACCOUNT IS LINKED.
THIS FAKE CLIENT USES THE DATA HARDCODED IN ./data/mock/sim_data.txt
"""
class SimulationClient(IGlucoseProvider):
    pass