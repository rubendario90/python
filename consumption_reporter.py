"""
Consumption Reporter for Calculator Usage Tracking
Tracks and reports usage statistics for calculator operations.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class ConsumptionReporter:
    """Tracks and reports calculator usage consumption."""
    
    def __init__(self, data_file: str = "consumption_data.json"):
        """Initialize the consumption reporter.
        
        Args:
            data_file: Path to the JSON file storing consumption data
        """
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load consumption data from file or create new structure."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default structure
        return {
            "total_operations": 0,
            "operations_by_type": {
                "suma": 0,
                "resta": 0,
                "multiplicacion": 0,
                "division": 0
            },
            "errors": {
                "division_por_cero": 0,
                "operacion_invalida": 0,
                "entrada_invalida": 0
            },
            "sessions": [],
            "first_use": None,
            "last_use": None
        }
    
    def _save_data(self) -> None:
        """Save consumption data to file."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.data_file)), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ Warning: Could not save consumption data: {e}")
    
    def track_operation(self, operation: str, num1: float = None, num2: float = None, 
                       result: Any = None, success: bool = True) -> None:
        """Track a calculator operation.
        
        Args:
            operation: Type of operation ('suma', 'resta', 'multiplicacion', 'division', 'salir')
            num1: First number (if applicable)
            num2: Second number (if applicable)
            result: Operation result
            success: Whether operation was successful
        """
        timestamp = datetime.now().isoformat()
        
        # Update first/last use
        if self.data["first_use"] is None:
            self.data["first_use"] = timestamp
        self.data["last_use"] = timestamp
        
        # Track successful operations
        if success and operation in self.data["operations_by_type"]:
            self.data["total_operations"] += 1
            self.data["operations_by_type"][operation] += 1
        
        # Log session entry
        session_entry = {
            "timestamp": timestamp,
            "operation": operation,
            "success": success
        }
        
        if num1 is not None:
            session_entry["num1"] = num1
        if num2 is not None:
            session_entry["num2"] = num2
        if result is not None:
            session_entry["result"] = str(result)
        
        self.data["sessions"].append(session_entry)
        
        # Keep only last 100 session entries to prevent file bloat
        if len(self.data["sessions"]) > 100:
            self.data["sessions"] = self.data["sessions"][-100:]
        
        self._save_data()
    
    def track_error(self, error_type: str) -> None:
        """Track an error occurrence.
        
        Args:
            error_type: Type of error ('division_por_cero', 'operacion_invalida', 'entrada_invalida')
        """
        if error_type in self.data["errors"]:
            self.data["errors"][error_type] += 1
        
        self.track_operation("error", success=False)
    
    def generate_report(self) -> str:
        """Generate a consumption report.
        
        Returns:
            Formatted string report of consumption data
        """
        report = []
        report.append("📊 REPORTE DE CONSUMO DE CALCULADORA")
        report.append("=" * 45)
        
        # Basic statistics
        total_ops = self.data["total_operations"]
        report.append(f"📈 Total de operaciones: {total_ops}")
        
        if self.data["first_use"]:
            first_use = datetime.fromisoformat(self.data["first_use"]).strftime("%Y-%m-%d %H:%M")
            report.append(f"🕐 Primer uso: {first_use}")
        
        if self.data["last_use"]:
            last_use = datetime.fromisoformat(self.data["last_use"]).strftime("%Y-%m-%d %H:%M")
            report.append(f"🕐 Último uso: {last_use}")
        
        # Operations breakdown
        report.append("\n🔢 Operaciones por tipo:")
        for op_type, count in self.data["operations_by_type"].items():
            percentage = (count / total_ops * 100) if total_ops > 0 else 0
            report.append(f"   {op_type.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Error statistics
        total_errors = sum(self.data["errors"].values())
        report.append(f"\n❌ Total de errores: {total_errors}")
        
        if total_errors > 0:
            report.append("   Tipos de errores:")
            for error_type, count in self.data["errors"].items():
                if count > 0:
                    error_name = error_type.replace("_", " ").title()
                    report.append(f"   - {error_name}: {count}")
        
        # Recent activity
        recent_sessions = self.data["sessions"][-5:]
        if recent_sessions:
            report.append("\n📝 Actividad reciente:")
            for session in recent_sessions:
                timestamp = datetime.fromisoformat(session["timestamp"]).strftime("%H:%M")
                operation = session["operation"]
                status = "✅" if session["success"] else "❌"
                report.append(f"   {timestamp} - {operation} {status}")
        
        return "\n".join(report)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for consumption.
        
        Returns:
            Dictionary with key consumption metrics
        """
        total_errors = sum(self.data["errors"].values())
        total_sessions = len(self.data["sessions"])
        
        return {
            "total_operations": self.data["total_operations"],
            "total_errors": total_errors,
            "total_sessions": total_sessions,
            "success_rate": (self.data["total_operations"] / total_sessions * 100) if total_sessions > 0 else 0,
            "most_used_operation": max(self.data["operations_by_type"], key=self.data["operations_by_type"].get) if self.data["total_operations"] > 0 else None
        }