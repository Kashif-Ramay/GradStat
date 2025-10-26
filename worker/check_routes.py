#!/usr/bin/env python3
"""Check if routes are registered"""

try:
    print("Loading app...")
    from analyze import app
    print("✅ App loaded successfully")
    
    print("\n📋 Registered routes:")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            methods = getattr(route, 'methods', set())
            print(f"  {methods} {route.path}")
    
    # Check specifically for test-advisor routes
    paths = [route.path for route in app.routes if hasattr(route, 'path')]
    
    if '/test-advisor/recommend' in paths:
        print("\n✅ Test Advisor endpoint is registered!")
    else:
        print("\n❌ Test Advisor endpoint NOT found!")
        print("Available paths:", paths)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
