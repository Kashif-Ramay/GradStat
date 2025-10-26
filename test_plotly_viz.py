"""
Test Script for Plotly Visualizations
Sprint 2.4 - Enhanced Visualizations
"""

import pandas as pd
import numpy as np
import sys
sys.path.append('worker')

from visualization import (
    create_scatter_plot,
    create_box_plot,
    create_line_plot,
    create_histogram,
    create_bar_plot,
    create_heatmap,
    create_qq_plot
)

def test_scatter_plot():
    """Test scatter plot creation"""
    print("\n" + "="*60)
    print("TEST 1: Scatter Plot")
    print("="*60)
    
    try:
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [2, 4, 5, 4, 5, 7, 8, 9, 10, 11]
        
        plot = create_scatter_plot(
            x=x,
            y=y,
            title='Test Scatter Plot',
            x_label='X Variable',
            y_label='Y Variable',
            theme='default'
        )
        
        print(f"✓ Scatter plot created")
        print(f"  Type: {plot['type']}")
        print(f"  Interactive: {plot.get('interactive', False)}")
        print(f"  Has data: {bool(plot.get('data'))}")
        print(f"  Title: {plot['title']}")
        
        print("\n✅ SCATTER PLOT TEST PASSED!")
        return True
    except Exception as e:
        print(f"\n❌ SCATTER PLOT TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_box_plot():
    """Test box plot creation"""
    print("\n" + "="*60)
    print("TEST 2: Box Plot")
    print("="*60)
    
    try:
        df = pd.DataFrame({
            'group': ['A']*10 + ['B']*10 + ['C']*10,
            'value': np.random.normal(50, 10, 10).tolist() + 
                     np.random.normal(60, 10, 10).tolist() + 
                     np.random.normal(70, 10, 10).tolist()
        })
        
        plot = create_box_plot(
            data=df,
            value_col='value',
            group_col='group',
            title='Test Box Plot',
            y_label='Value',
            theme='colorblind'
        )
        
        print(f"✓ Box plot created")
        print(f"  Type: {plot['type']}")
        print(f"  Interactive: {plot.get('interactive', False)}")
        print(f"  Has data: {bool(plot.get('data'))}")
        
        print("\n✅ BOX PLOT TEST PASSED!")
        return True
    except Exception as e:
        print(f"\n❌ BOX PLOT TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_line_plot():
    """Test line plot creation"""
    print("\n" + "="*60)
    print("TEST 3: Line Plot")
    print("="*60)
    
    try:
        x = list(range(1, 11))
        y = [2, 4, 5, 4, 5, 7, 8, 9, 10, 11]
        error = [0.5, 0.6, 0.7, 0.5, 0.6, 0.8, 0.7, 0.9, 0.8, 1.0]
        
        plot = create_line_plot(
            x=x,
            y=y,
            title='Test Line Plot',
            x_label='Time',
            y_label='Value',
            error=error,
            theme='scientific'
        )
        
        print(f"✓ Line plot created")
        print(f"  Type: {plot['type']}")
        print(f"  Interactive: {plot.get('interactive', False)}")
        print(f"  Has data: {bool(plot.get('data'))}")
        
        print("\n✅ LINE PLOT TEST PASSED!")
        return True
    except Exception as e:
        print(f"\n❌ LINE PLOT TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_histogram():
    """Test histogram creation"""
    print("\n" + "="*60)
    print("TEST 4: Histogram")
    print("="*60)
    
    try:
        data = np.random.normal(50, 10, 100).tolist()
        
        plot = create_histogram(
            data=data,
            title='Test Histogram',
            x_label='Value',
            y_label='Frequency',
            bins=20,
            theme='vibrant'
        )
        
        print(f"✓ Histogram created")
        print(f"  Type: {plot['type']}")
        print(f"  Interactive: {plot.get('interactive', False)}")
        print(f"  Has data: {bool(plot.get('data'))}")
        
        print("\n✅ HISTOGRAM TEST PASSED!")
        return True
    except Exception as e:
        print(f"\n❌ HISTOGRAM TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_heatmap():
    """Test heatmap creation"""
    print("\n" + "="*60)
    print("TEST 5: Heatmap")
    print("="*60)
    
    try:
        df = pd.DataFrame(
            np.random.rand(5, 5),
            columns=['A', 'B', 'C', 'D', 'E'],
            index=['V1', 'V2', 'V3', 'V4', 'V5']
        )
        
        plot = create_heatmap(
            data=df,
            title='Test Heatmap',
            x_label='Variables',
            y_label='Variables',
            theme='default'
        )
        
        print(f"✓ Heatmap created")
        print(f"  Type: {plot['type']}")
        print(f"  Interactive: {plot.get('interactive', False)}")
        print(f"  Has data: {bool(plot.get('data'))}")
        
        print("\n✅ HEATMAP TEST PASSED!")
        return True
    except Exception as e:
        print(f"\n❌ HEATMAP TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_qq_plot():
    """Test Q-Q plot creation"""
    print("\n" + "="*60)
    print("TEST 6: Q-Q Plot")
    print("="*60)
    
    try:
        data = np.random.normal(0, 1, 100).tolist()
        
        plot = create_qq_plot(
            data=data,
            title='Test Q-Q Plot',
            theme='grayscale'
        )
        
        print(f"✓ Q-Q plot created")
        print(f"  Type: {plot['type']}")
        print(f"  Interactive: {plot.get('interactive', False)}")
        print(f"  Has data: {bool(plot.get('data'))}")
        
        print("\n✅ Q-Q PLOT TEST PASSED!")
        return True
    except Exception as e:
        print(f"\n❌ Q-Q PLOT TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_themes():
    """Test all themes"""
    print("\n" + "="*60)
    print("TEST 7: Themes")
    print("="*60)
    
    try:
        themes = ['default', 'colorblind', 'grayscale', 'vibrant', 'scientific']
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 3, 5, 6]
        
        for theme in themes:
            plot = create_scatter_plot(x, y, title=f'{theme} theme', theme=theme)
            print(f"✓ {theme} theme works")
        
        print("\n✅ THEMES TEST PASSED!")
        return True
    except Exception as e:
        print(f"\n❌ THEMES TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 TESTING PLOTLY VISUALIZATIONS")
    print("Sprint 2.4 - Enhanced Visualizations")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Scatter Plot", test_scatter_plot()))
    results.append(("Box Plot", test_box_plot()))
    results.append(("Line Plot", test_line_plot()))
    results.append(("Histogram", test_histogram()))
    results.append(("Heatmap", test_heatmap()))
    results.append(("Q-Q Plot", test_qq_plot()))
    results.append(("Themes", test_themes()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Plotly visualizations ready!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Review errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
