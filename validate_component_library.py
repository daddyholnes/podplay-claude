#!/usr/bin/env python3
"""
Component Library Validation Test
Tests the shared component library structure and mem0.ai integration
"""

import json
import os
import sys
from pathlib import Path

def test_component_library_structure():
    """Test that the component library has the correct structure"""
    base_path = Path("/home/woody/Documents/podplay-claude/shared-components")
    
    required_files = [
        "package.json",
        "tsconfig.json", 
        "README.md",
        "registry.json",
        "src/index.ts",
        "src/registry.ts",
        "src/types/index.ts",
        "src/utils/cn.ts",
        "src/components/effects/AuroraBackground.tsx",
        "src/components/effects/BackgroundGradientAnimation.tsx", 
        "src/components/effects/SplashCursor.tsx",
        "src/components/ui/GlowingEffect.tsx",
        "src/components/sanctuary/SanctuaryLayout.tsx",
        "docs/components/AuroraBackground.md",
        "docs/components/SanctuaryLayout.md"
    ]
    
    print("🧪 Testing Component Library Structure...")
    
    missing_files = []
    for file_path in required_files:
        full_path = base_path / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def test_registry_json():
    """Test that the registry.json is valid and complete"""
    registry_path = Path("/home/woody/Documents/podplay-claude/shared-components/registry.json")
    
    print("🧪 Testing Component Registry...")
    
    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
        
        # Test required structure
        required_keys = ["library", "components", "aiIntegration", "searchPatterns"]
        for key in required_keys:
            if key not in registry:
                print(f"❌ Missing key in registry: {key}")
                return False
        
        # Test components
        components = registry["components"]
        expected_components = ["AuroraBackground", "BackgroundGradientAnimation", "SplashCursor", "GlowingEffect", "SanctuaryLayout"]
        
        found_components = [comp["name"] for comp in components]
        for expected in expected_components:
            if expected not in found_components:
                print(f"❌ Missing component in registry: {expected}")
                return False
        
        print(f"✅ Registry valid with {len(components)} components")
        return True
        
    except Exception as e:
        print(f"❌ Registry validation failed: {e}")
        return False

def test_package_json():
    """Test that package.json is properly configured"""
    package_path = Path("/home/woody/Documents/podplay-claude/shared-components/package.json")
    
    print("🧪 Testing Package Configuration...")
    
    try:
        with open(package_path, 'r') as f:
            package = json.load(f)
        
        required_fields = ["name", "version", "description", "main", "types", "exports"]
        for field in required_fields:
            if field not in package:
                print(f"❌ Missing field in package.json: {field}")
                return False
        
        # Check if name matches expected
        if package["name"] != "@podplay/sanctuary-components":
            print(f"❌ Incorrect package name: {package['name']}")
            return False
            
        print("✅ Package.json properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Package.json validation failed: {e}")
        return False

def test_component_exports():
    """Test that main index.ts exports all components"""
    index_path = Path("/home/woody/Documents/podplay-claude/shared-components/src/index.ts")
    
    print("🧪 Testing Component Exports...")
    
    try:
        with open(index_path, 'r') as f:
            content = f.read()
        
        expected_exports = [
            "AuroraBackground",
            "BackgroundGradientAnimation", 
            "SplashCursor",
            "GlowingEffect",
            "SanctuaryLayout",
            "cn",
            "COMPONENT_REGISTRY"
        ]
        
        for export in expected_exports:
            if export not in content:
                print(f"❌ Missing export: {export}")
                return False
        
        print("✅ All components properly exported")
        return True
        
    except Exception as e:
        print(f"❌ Export validation failed: {e}")
        return False

def test_mem0_integration():
    """Test mem0.ai integration structure"""
    registry_path = Path("/home/woody/Documents/podplay-claude/shared-components/registry.json")
    
    print("🧪 Testing Mem0.ai Integration...")
    
    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
        
        # Check AI integration section
        ai_integration = registry.get("aiIntegration", {})
        required_ai_fields = ["mem0Compatible", "searchableByTags", "contextAware", "codeGeneration"]
        
        for field in required_ai_fields:
            if field not in ai_integration:
                print(f"❌ Missing AI integration field: {field}")
                return False
        
        # Check search patterns
        search_patterns = registry.get("searchPatterns", [])
        if len(search_patterns) < 5:
            print(f"❌ Insufficient search patterns: {len(search_patterns)}")
            return False
        
        # Check component metadata
        for component in registry["components"]:
            required_meta = ["name", "category", "description", "useCases", "codeExample", "keywords"]
            for field in required_meta:
                if field not in component:
                    print(f"❌ Component {component.get('name', 'unknown')} missing: {field}")
                    return False
        
        print("✅ Mem0.ai integration properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Mem0 integration test failed: {e}")
        return False

def run_all_tests():
    """Run all component library tests"""
    print("🚀 Running Component Library Validation Tests\n")
    
    tests = [
        ("Component Library Structure", test_component_library_structure),
        ("Registry JSON", test_registry_json),
        ("Package Configuration", test_package_json),
        ("Component Exports", test_component_exports),
        ("Mem0.ai Integration", test_mem0_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}\n")
    
    # Summary
    print("=" * 50)
    print(f"🎯 Component Library Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Component library is ready for mem0.ai integration")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please fix issues before proceeding.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
