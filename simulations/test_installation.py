"""
VERIFICATION SCRIPT - Tests that the CDG framework works
Run this first to ensure everything is set up correctly
"""

import sys
import importlib

def test_imports():
    """Test that all required packages can be imported"""
    packages = ['numpy', 'scipy', 'matplotlib', 'networkx']
    
    print("🔧 Testing package imports...")
    for package in packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ FAILED to import {package}: {e}")
            return False
    
    return True

def test_basic_functionality():
    """Test basic CDG functionality"""
    try:
        # Test basic imports from our framework
        from simulations.basic_emotion_space import EmotionSpace
        from simulations.simple_curvature_demo import CurvatureDemo
        from simulations.insight_demo import InsightDemo
        
        print("✅ CDG modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ CDG module import failed: {e}")
        return False

def test_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version compatible")
        return True
    else:
        print("❌ Python 3.8 or higher required")
        return False

if __name__ == "__main__":
    print("🧪 CDG Framework Installation Test")
    print("=" * 50)
    
    tests = [
        test_python_version(),
        test_imports(), 
        test_basic_functionality()
    ]
    
    print("\n" + "=" * 50)
    if all(tests):
        print("🎉 ALL TESTS PASSED! Your CDG framework is ready.")
        print("\nNext steps:")
        print("1. Run: python simulations/basic_emotion_space.py")
        print("2. Then: python simulations/run_verified.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Check Python version: python --version")
        print("- Ensure you're in the CDG-Framework directory")
