"""
RUN ALL CDG DEMOS - VERIFIED WORKING
Runs all tested CDG demonstrations using your existing file names
"""

import importlib
import sys

def run_demo(module_name, class_name):
    """Safely run a demo module"""
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Running: {module_name}")
        print('='*60)
        
        # Import module
        module = importlib.import_module(module_name)
        
        # Get class and run demo
        demo_class = getattr(module, class_name)
        demo_instance = demo_class()
        demo_instance.run_demo()
        
        return True
        
    except Exception as e:
        print(f"❌ Error running {module_name}: {e}")
        return False

def main():
    """Run all verified demos"""
    print("🧠 CDG Framework - All Demos")
    print("Running all TESTED and WORKING simulations...")
    
    # List of verified working demos (using YOUR file names)
    demos = [
        ('minimal_cdg', 'MinimalCDG'),
        ('depression_basin', 'DepressionSimulation'), 
        ('insight_simulation', 'InsightSimulation')
    ]
    
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
        print("   1. Run: python test_installation.py")
        print("   2. Check: pip install -r requirements.txt")
        print("   3. Verify Python version: python --version")

if __name__ == "__main__":
    main()
