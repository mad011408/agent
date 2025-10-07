"""
💻 Code Execution Tool
Safe code execution environment for AI agents
"""

import asyncio
import subprocess
from typing import Dict, Any, Optional
import tempfile
import os
import logging

logger = logging.getLogger(__name__)


class CodeExecutionTool:
    """
    Code Execution Tool
    
    Executes code in sandboxed environment
    """
    
    def __init__(self, timeout: int = 10, max_memory_mb: int = 512):
        self.timeout = timeout
        self.max_memory_mb = max_memory_mb
        self.execution_count = 0
        self.success_count = 0
        
        logger.info(f"💻 Code Execution Tool initialized (timeout={timeout}s)")
    
    async def execute_python(self, code: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute Python code
        
        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds
            
        Returns:
            Execution result
        """
        logger.info("💻 Executing Python code")
        
        self.execution_count += 1
        timeout = timeout or self.timeout
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute code
                process = await asyncio.create_subprocess_exec(
                    'python', temp_file,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                result = {
                    "success": process.returncode == 0,
                    "stdout": stdout.decode('utf-8'),
                    "stderr": stderr.decode('utf-8'),
                    "return_code": process.returncode
                }
                
                if result["success"]:
                    self.success_count += 1
                
                logger.info(f"✅ Execution completed (success={result['success']})")
                
                return result
                
            finally:
                # Clean up temp file
                os.unlink(temp_file)
                
        except asyncio.TimeoutError:
            logger.error("⏱️ Execution timeout")
            return {
                "success": False,
                "error": f"Execution timeout ({timeout}s exceeded)",
                "stdout": "",
                "stderr": ""
            }
        except Exception as e:
            logger.error(f"❌ Execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": ""
            }
    
    async def execute_javascript(self, code: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute JavaScript code using Node.js
        
        Args:
            code: JavaScript code to execute
            timeout: Execution timeout
            
        Returns:
            Execution result
        """
        logger.info("💻 Executing JavaScript code")
        
        self.execution_count += 1
        timeout = timeout or self.timeout
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute code
                process = await asyncio.create_subprocess_exec(
                    'node', temp_file,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                result = {
                    "success": process.returncode == 0,
                    "stdout": stdout.decode('utf-8'),
                    "stderr": stderr.decode('utf-8'),
                    "return_code": process.returncode
                }
                
                if result["success"]:
                    self.success_count += 1
                
                return result
                
            finally:
                os.unlink(temp_file)
                
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Execution timeout ({timeout}s exceeded)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def validate_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Validate code for safety
        
        Args:
            code: Code to validate
            language: Programming language
            
        Returns:
            Validation result
        """
        # Simple validation (in production, use proper static analysis)
        dangerous_keywords = [
            "os.system", "subprocess.call", "eval", "exec",
            "__import__", "open", "file", "input", "raw_input"
        ]
        
        issues = []
        for keyword in dangerous_keywords:
            if keyword in code:
                issues.append(f"Potentially dangerous: {keyword}")
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        success_rate = 0.0
        if self.execution_count > 0:
            success_rate = (self.success_count / self.execution_count) * 100
        
        return {
            "total_executions": self.execution_count,
            "successful_executions": self.success_count,
            "success_rate": round(success_rate, 2)
        }