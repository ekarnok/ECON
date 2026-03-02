import time
import random

# --- DATA MODELS ---

MATERIAL_LIBRARY = {
    "Adobe": {"insulation": 0.9, "wind_res": 0.7, "flood_res": 0.2, "cost": 10},
    "Bamboo": {"insulation": 0.3, "wind_res": 0.9, "flood_res": 0.8, "cost": 15},
    "Stone": {"insulation": 0.8, "wind_res": 1.0, "flood_res": 0.9, "cost": 50},
    "Timber": {"insulation": 0.6, "wind_res": 0.6, "flood_res": 0.4, "cost": 30}
}

class Building:
    def __init__(self, name, material_type, height, windows_count):
        self.name = name
        self.mat = MATERIAL_LIBRARY[material_type]
        self.mat_name = material_type
        self.height = height # 1-5 meters
        self.windows = windows_count # Affects ventilation vs heat
        self.integrity = 100.0
        self.comfort_score = 100.0

# --- SIMULATION ENGINE ---

def run_simulation(building, biome_hazards):
    print(f"\n--- 🏗️ SIMULATING: {building.name} ({building.mat_name}) ---")
    years = [5, 10, 20, 50]
    current_year = 0
    
    for target_year in years:
        # Simulate gap years
        while current_year < target_year:
            current_year += 1
            
            # Physics Calculations
            # 1. Heat Stress: Windows help ventilation but hurt insulation if too many
            ventilation_mod = building.windows * 0.05
            heat_impact = biome_hazards['heat'] * (1 - (building.mat['insulation'] + ventilation_mod))
            
            # 2. Wind Stress: Higher buildings take more damage unless material is flexible
            wind_impact = (biome_hazards['wind'] * building.height) * (1 - building.mat['wind_res'])
            
            # 3. Flood Stress: Height is the primary defense
            flood_impact = max(0, biome_hazards['flood'] - (building.height * 2)) * (1 - building.mat['flood_res'])
            
            # Apply total degradation
            yearly_wear = (heat_impact + wind_impact + flood_impact) * 0.5
            building.integrity -= yearly_wear
            
            # Calculate Comfort (Occupant Health)
            # Ideal is balanced ventilation
            building.comfort_score = 100 - abs(building.windows - 4) * 10 - (heat_impact * 2)

        # Output Results at Checkpoints
        print(f"Year {current_year}: Integrity {max(0, round(building.integrity, 1))}% | Comfort {max(0, round(building.comfort_score, 1))}%")
        
        if building.integrity <= 0:
            print("❌ CRITICAL FAILURE: Structure collapsed before year 50.")
            return False

    # Final Scoring
    final_score = (building.integrity + building.comfort_score) / 2
    print(f"\n--- FINAL RESILIENCE SCORE: {round(final_score, 2)}% ---")
    
    if final_score >= 90:
        print("🏆 WIN CONDITION: You have mastered Vernacular Architecture!")
    else:
        print("📝 RESULTS: Your design survived, but failed to reach 100% efficiency.")
    return True

# --- MAIN GAME LOOP ---

def main():
    print("Welcome to VERNACULA. Design for the environment.")
    
    # Simple User Input
    print("\nSelect Material: Adobe, Bamboo, Stone, Timber")
    choice = input("Material > ")
    if choice not in MATERIAL_LIBRARY: choice = "Timber"
    
    h = float(input("Building Height (1-5 meters) > "))
    w = int(input("Number of Windows (1-10) > "))
    
    # Define Biome Hazards (Heat, Wind, Flood intensity 1-10)
    # Example: Tropical Monsoon
    monsoon_hazards = {'heat': 7, 'wind': 8, 'flood': 9}
    
    player_house = Building("Player Home", choice, h, w)
    run_simulation(player_house, monsoon_hazards)

if __name__ == "__main__":
    main()
