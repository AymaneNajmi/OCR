#!/usr/bin/env python
"""
Simple launcher script to start the Streamlit Food-IA app.
Usage: python run_app.py
Or: streamlit run app.py
"""

import subprocess
import sys
import os

def run_streamlit_app():
    """Launch the Streamlit app with proper path setup."""
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(current_dir, 'app.py')
    
    print("=" * 60)
    print("🍽️  Starting Food-IA Streamlit App...")
    print("=" * 60)
    print(f"\nApp file: {app_file}")
    print("\nThe app will open in your browser shortly.")
    print("Press Ctrl+C to stop the server.\n")
    
    # Launch Streamlit
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", app_file],
            cwd=current_dir
        )
    except KeyboardInterrupt:
        print("\n\n✅ Food-IA app stopped.")
    except Exception as e:
        print(f"\n❌ Error running app: {e}")
        print("\nMake sure you have Streamlit installed:")
        print("  pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    run_streamlit_app()
