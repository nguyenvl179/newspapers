# -*- coding: utf-8 -*-

from .context import papers

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(papers.hmm())


if __name__ == '__main__':
    unittest.main()
