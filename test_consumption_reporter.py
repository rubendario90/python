"""
Tests for the ConsumptionReporter class
"""

import os
import json
import tempfile
import unittest
from datetime import datetime
from consumption_reporter import ConsumptionReporter


class TestConsumptionReporter(unittest.TestCase):
    """Test cases for ConsumptionReporter functionality."""
    
    def setUp(self):
        """Set up test environment with temporary file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.reporter = ConsumptionReporter(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_initial_data_structure(self):
        """Test that initial data structure is correct."""
        data = self.reporter.data
        
        self.assertEqual(data["total_operations"], 0)
        self.assertIn("operations_by_type", data)
        self.assertIn("errors", data)
        self.assertIn("sessions", data)
        self.assertIsNone(data["first_use"])
        self.assertIsNone(data["last_use"])
        
        # Check operation types
        expected_ops = {"suma", "resta", "multiplicacion", "division"}
        self.assertEqual(set(data["operations_by_type"].keys()), expected_ops)
        
        # Check error types
        expected_errors = {"division_por_cero", "operacion_invalida", "entrada_invalida"}
        self.assertEqual(set(data["errors"].keys()), expected_errors)
    
    def test_track_operation(self):
        """Test tracking of operations."""
        # Track a successful operation
        self.reporter.track_operation("suma", 5, 3, 8, success=True)
        
        data = self.reporter.data
        self.assertEqual(data["total_operations"], 1)
        self.assertEqual(data["operations_by_type"]["suma"], 1)
        self.assertIsNotNone(data["first_use"])
        self.assertIsNotNone(data["last_use"])
        self.assertEqual(len(data["sessions"]), 1)
        
        # Check session data
        session = data["sessions"][0]
        self.assertEqual(session["operation"], "suma")
        self.assertEqual(session["num1"], 5)
        self.assertEqual(session["num2"], 3)
        self.assertEqual(session["result"], "8")
        self.assertTrue(session["success"])
    
    def test_track_multiple_operations(self):
        """Test tracking multiple operations."""
        operations = [
            ("suma", 1, 2, 3),
            ("resta", 5, 3, 2),
            ("multiplicacion", 4, 5, 20),
            ("division", 10, 2, 5)
        ]
        
        for op, n1, n2, result in operations:
            self.reporter.track_operation(op, n1, n2, result, success=True)
        
        data = self.reporter.data
        self.assertEqual(data["total_operations"], 4)
        self.assertEqual(data["operations_by_type"]["suma"], 1)
        self.assertEqual(data["operations_by_type"]["resta"], 1)
        self.assertEqual(data["operations_by_type"]["multiplicacion"], 1)
        self.assertEqual(data["operations_by_type"]["division"], 1)
    
    def test_track_error(self):
        """Test error tracking."""
        self.reporter.track_error("division_por_cero")
        
        data = self.reporter.data
        self.assertEqual(data["errors"]["division_por_cero"], 1)
        self.assertEqual(data["total_operations"], 0)  # Errors don't count as operations
        self.assertEqual(len(data["sessions"]), 1)
        
        # Check error session
        session = data["sessions"][0]
        self.assertEqual(session["operation"], "error")
        self.assertFalse(session["success"])
    
    def test_data_persistence(self):
        """Test that data is saved and loaded correctly."""
        # Track some operations
        self.reporter.track_operation("suma", 1, 1, 2, success=True)
        self.reporter.track_error("operacion_invalida")
        
        # Create new reporter with same file
        reporter2 = ConsumptionReporter(self.temp_file.name)
        
        # Verify data was loaded
        self.assertEqual(reporter2.data["total_operations"], 1)
        self.assertEqual(reporter2.data["operations_by_type"]["suma"], 1)
        self.assertEqual(reporter2.data["errors"]["operacion_invalida"], 1)
        self.assertEqual(len(reporter2.data["sessions"]), 2)
    
    def test_generate_report(self):
        """Test report generation."""
        # Track some operations and errors
        self.reporter.track_operation("suma", 1, 2, 3, success=True)
        self.reporter.track_operation("resta", 5, 3, 2, success=True)
        self.reporter.track_error("division_por_cero")
        
        report = self.reporter.generate_report()
        
        # Check that report contains expected sections
        self.assertIn("REPORTE DE CONSUMO", report)
        self.assertIn("Total de operaciones: 2", report)
        self.assertIn("Operaciones por tipo:", report)
        self.assertIn("Total de errores: 1", report)
        self.assertIn("Actividad reciente:", report)
        self.assertIn("suma", report)
        self.assertIn("resta", report)
    
    def test_get_summary_stats(self):
        """Test summary statistics."""
        # Track operations and errors
        for _ in range(3):
            self.reporter.track_operation("suma", 1, 1, 2, success=True)
        self.reporter.track_operation("resta", 5, 3, 2, success=True)
        self.reporter.track_error("operacion_invalida")
        
        stats = self.reporter.get_summary_stats()
        
        self.assertEqual(stats["total_operations"], 4)
        self.assertEqual(stats["total_errors"], 1)
        self.assertEqual(stats["total_sessions"], 5)
        self.assertEqual(stats["success_rate"], 80.0)  # 4/5 * 100
        self.assertEqual(stats["most_used_operation"], "suma")
    
    def test_session_limit(self):
        """Test that sessions are limited to 100 entries."""
        # Track more than 100 operations
        for i in range(105):
            self.reporter.track_operation("suma", i, 1, i+1, success=True)
        
        # Should only keep last 100 sessions
        self.assertEqual(len(self.reporter.data["sessions"]), 100)
        
        # First session should be from operation 6 (105-100+1)
        first_session = self.reporter.data["sessions"][0]
        self.assertEqual(first_session["num1"], 5)  # 0-indexed, so 5 is the 6th operation


if __name__ == "__main__":
    unittest.main()