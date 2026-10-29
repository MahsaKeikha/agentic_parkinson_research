import unittest
from check_submission import validate

class TestSubmissionPreflight(unittest.TestCase):
    def test_missing_citation_fails(self):
        r=validate(r"\cite{unknown}", "@article{known,\n title={Title}\n}")
        self.assertFalse(r["ok"])
    def test_duplicate_key_fails(self):
        r=validate("v3", "@article{a,}\n@article{a,}")
        self.assertFalse(r["ok"])
    def test_strict_requires_complete_bibliography(self):
        r=validate("v3", "@article{a, title={Title}}", strict=True)
        self.assertFalse(r["ok"])
    def test_non_strict_preflight_allows_research_draft(self):
        r=validate("v3", "@article{a, title={Title}}")
        self.assertTrue(r["ok"])
        self.assertTrue(r["warnings"])

if __name__=="__main__":
    unittest.main()
