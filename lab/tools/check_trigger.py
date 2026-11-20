"""Check one trigger file before the screen registers it: header, output and look-ahead.
Usage (from the repo root): python lab/tools/check_trigger.py NAME"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import screen

if __name__ == "__main__":
    probs = screen.validate_trigger(sys.argv[1])
    print("OK: header valid, fires, no look-ahead" if not probs else "PROBLEMS:\n- " + "\n- ".join(probs))
    sys.exit(1 if probs else 0)
