"""Test the _update_index_skills_section regex replacement logic."""
import sys, os, tempfile, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add skill-forge scripts to path
skill_forge = r"D:\workspace\misc\skills\huawei-auto-pal\skill-forge\scripts"
sys.path.insert(0, skill_forge)
import register

# Create a fake index.html with a skills section
tmp = tempfile.mkdtemp(prefix="idx_test_")
index_path = os.path.join(tmp, "index.html")

# Test 1: index.html with existing skills section (replace)
html_with_section = """<!DOCTYPE html>
<html><body>
<h1>Dashboard</h1>
<div class="horizon-grid">cards</div>
<div class="skills-section">
  <h2>Proposed skills &amp; memory (1)</h2>
  <div class="skill-card">old content</div>
</div>
</div>
</body></html>"""

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_with_section)

# Patch _build_skills_section to return new HTML
import unittest.mock as mock
new_skills_html = '<div class="skills-section"><h2>NEW</h2><div class="skill-card">new</div></div>'
with mock.patch.object(register, "_build_skills_section", return_value=new_skills_html):
    register._update_index_skills_section(tmp)

with open(index_path, encoding="utf-8") as f:
    result = f.read()
print("=== Test 1: Replace existing section ===")
print(result)
print("PASS: old section replaced" if "NEW" in result and "old content" not in result else "FAIL: replacement failed")

# Test 2: index.html without skills section (inject before </body>)
html_without_section = """<!DOCTYPE html>
<html><body>
<h1>Dashboard</h1>
<div class="horizon-grid">cards</div>
</body></html>"""

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_without_section)

with mock.patch.object(register, "_build_skills_section", return_value=new_skills_html):
    register._update_index_skills_section(tmp)

with open(index_path, encoding="utf-8") as f:
    result = f.read()
print("\n=== Test 2: Inject before </body> ===")
print(result)
print("PASS: section injected" if "NEW" in result and result.index("NEW") < result.index("</body>") else "FAIL: injection failed")

# Test 3: No index.html at all
os.unlink(index_path)
print("\n=== Test 3: No index.html ===")
with mock.patch.object(register, "_build_skills_section", return_value=new_skills_html):
    register._update_index_skills_section(tmp)
print("PASS: no crash" if not os.path.exists(index_path) else "FAIL: should not create file")

# Test 4: _build_skills_section returns empty string
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_without_section)
with mock.patch.object(register, "_build_skills_section", return_value=""):
    register._update_index_skills_section(tmp)
with open(index_path, encoding="utf-8") as f:
    result = f.read()
print("\n=== Test 4: Empty skills section ===")
print("PASS: unchanged" if "NEW" not in result else "FAIL: should not inject empty")

import shutil
shutil.rmtree(tmp, ignore_errors=True)
