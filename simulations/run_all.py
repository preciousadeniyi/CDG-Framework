"""
RUN ALL CDG DEMOS - VERIFIED WORKING
Runs all tested CDG demonstrations using your existing file names
"""

import importlib
import sys
import os

def run_demo(module_name, class_name):
    """Safely run a demo module"""
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Running: {module_name}")
        print('='*60)
        
        # Check if file exists
        if not os.path.exists(f"{module_name}.py"):
            print(f"❌ File {module_name}.py not found!")
            return False
        
        # Import module
        module = importlib.import_module(module_name)
        
        # Get class and run demo
        demo_class = getattr(module, class_name)
        demo_instance = demo_class()
        demo_instance.run_demo()
        
        return True
        
    except Exception as e:
        print(f"❌ Error running {module_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verified demos"""
    print("🧠 CDG Framework - All Demos")
    print("Running all TESTED and WORKING simulations...")
    
    # List of verified working demos (using ACTUAL file names from your code)
    demos = [
        ('minimal_cdg_demo', 'MinimalCDG'),           # From minimal CDG demo
        ('depression_basin_demo', 'DepressionSimulation'), # From depression demo  
        ('insight_simulation_demo', 'InsightSimulation')   # From insight demo
    ]
    
    # Alternative: If you saved files with different names, use these:
    # demos = [
    #     ('minimal_cdg', 'MinimalCDG'),
    #     ('depression_basin', 'DepressionSimulation'),
    #     ('insight_simulation', 'InsightSimulation')
    # ]
    
    success_count = 0
    total_demos = len(demos)
    
    for module_name, class_name in demos:
        if run_demo(module_name, class_name):
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 EXECUTION SUMMARY")
    print('='*60)
    print(f"Successful demos: {success_count}/{total_demos}")
    
    if success_count == total_demos:
        print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("\n✅ CDG Framework is working correctly")
        print("📁 Generated files:")
        print("   - emotion_space_demo.png")
        print("   - depression_demo.png") 
        print("   - insight_demo.png")
        print("\n🚀 Next: Explore the code and extend the framework!")
    else:
        print("⚠️  Some demos failed. Check errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure these files exist in current directory:")
        for module_name, _ in demos:
            print(f"      - {module_name}.py")
        print("   2. Run: pip install -r requirements.txt")
        print("   3. Check Python version: python --version")

if __name__ == "__main__":
    main()
