#!/usr/bin/env python3
"""
Email Task Manager Security Auditor Agent
Comprehensive security analysis and vulnerability detection
"""

import os
import re
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

class EmailTaskSecurityAuditor:
    """Specialized security auditor for Email Task Manager project"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_path = self.project_root / "backend"
        self.frontend_path = self.project_root / "frontend"
        
        self.findings = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'info': []
        }
        
        # Security patterns to check
        self.security_patterns = {
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']{3,}["\']',
                r'secret\s*=\s*["\'][^"\']{8,}["\']',
                r'api_key\s*=\s*["\'][^"\']{8,}["\']',
                r'token\s*=\s*["\'][^"\']{8,}["\']'
            ],
            'sql_injection': [
                r'query\s*=\s*["\'].*%s.*["\']',
                r'execute\s*\(["\'].*\+.*["\']',
                r'raw\s*\(["\'].*\+.*["\']'
            ],
            'xss_vulnerabilities': [
                r'innerHTML\s*=\s*[^;]+[^e]scape',
                r'dangerouslySetInnerHTML',
                r'document\.write\s*\([^)]*[^e]scape'
            ],
            'weak_crypto': [
                r'md5\s*\(',
                r'sha1\s*\(',
                r'base64\.encode\s*\(',
                r'simple.*encrypt'
            ]
        }
    
    def run_complete_audit(self) -> Dict[str, Any]:
        """Run comprehensive security audit"""
        print("🔍 Starting Email Task Manager Security Audit...")
        
        # Core security checks
        self._audit_authentication_system()
        self._audit_token_encryption()
        self._audit_input_validation()
        self._audit_rate_limiting()
        self._audit_cors_configuration()
        self._audit_session_security()
        self._audit_database_security()
        self._audit_api_endpoints()
        self._audit_environment_security()
        self._audit_dependency_vulnerabilities()
        
        # Advanced security analysis
        self._check_code_patterns()
        self._audit_file_permissions()
        self._check_security_headers()
        
        return self._generate_security_report()
    
    def _audit_authentication_system(self):
        """Audit OAuth and JWT implementation"""
        print("🔐 Auditing authentication system...")
        
        auth_file = self.backend_path / "routes" / "auth.py"
        if auth_file.exists():
            content = auth_file.read_text()
            
            # Check JWT configuration
            if 'JWT_ACCESS_TOKEN_EXPIRES' not in content and 'timedelta' not in content:
                self.findings['medium'].append({
                    'type': 'JWT Configuration',
                    'file': str(auth_file),
                    'issue': 'JWT token expiration not configured',
                    'recommendation': 'Set appropriate token expiration time'
                })
            
            # Check OAuth state validation
            if 'session[\'state\']' not in content:
                self.findings['high'].append({
                    'type': 'OAuth Security',
                    'file': str(auth_file),
                    'issue': 'OAuth state parameter not validated',
                    'recommendation': 'Implement CSRF protection with state parameter'
                })
            
            # Check secure redirect validation
            if 'redirect(' in content and 'validate_redirect' not in content:
                self.findings['medium'].append({
                    'type': 'Open Redirect',
                    'file': str(auth_file),
                    'issue': 'Potential open redirect vulnerability',
                    'recommendation': 'Validate redirect URLs against whitelist'
                })
    
    def _audit_token_encryption(self):
        """Audit token encryption implementation"""
        print("🔒 Auditing token encryption...")
        
        encryption_file = self.backend_path / "utils" / "encryption.py"
        if encryption_file.exists():
            content = encryption_file.read_text()
            
            # Check encryption algorithm
            if 'Fernet' in content:
                self.findings['info'].append({
                    'type': 'Encryption',
                    'file': str(encryption_file),
                    'issue': 'Using Fernet encryption (good)',
                    'recommendation': 'Ensure keys are rotated regularly'
                })
            
            # Check key derivation
            if 'PBKDF2HMAC' not in content:
                self.findings['high'].append({
                    'type': 'Key Derivation',
                    'file': str(encryption_file),
                    'issue': 'Not using PBKDF2 for key derivation',
                    'recommendation': 'Use PBKDF2HMAC for key derivation'
                })
            
            # Check iteration count
            iterations_match = re.search(r'iterations=(\d+)', content)
            if iterations_match:
                iterations = int(iterations_match.group(1))
                if iterations < 100000:
                    self.findings['medium'].append({
                        'type': 'Weak Key Derivation',
                        'file': str(encryption_file),
                        'issue': f'PBKDF2 iterations too low: {iterations}',
                        'recommendation': 'Use at least 100,000 iterations'
                    })
        else:
            self.findings['critical'].append({
                'type': 'Missing Encryption',
                'file': 'Backend',
                'issue': 'Token encryption not implemented',
                'recommendation': 'Implement token encryption for sensitive data'
            })
    
    def _audit_input_validation(self):
        """Audit input validation and sanitization"""
        print("🛡️ Auditing input validation...")
        
        validators_file = self.backend_path / "utils" / "validators.py"
        if validators_file.exists():
            content = validators_file.read_text()
            
            # Check HTML escaping
            if 'html.escape' not in content:
                self.findings['high'].append({
                    'type': 'XSS Protection',
                    'file': str(validators_file),
                    'issue': 'HTML escaping not implemented',
                    'recommendation': 'Use html.escape() for all user inputs'
                })
            
            # Check length limits
            if 'max_length' not in content:
                self.findings['medium'].append({
                    'type': 'Input Limits',
                    'file': str(validators_file),
                    'issue': 'Input length limits not enforced',
                    'recommendation': 'Implement length limits for all text inputs'
                })
        
        # Check route validation
        route_files = list(self.backend_path.glob("routes/*.py"))
        for route_file in route_files:
            content = route_file.read_text()
            
            # Check for direct request.json usage without validation
            if 'request.json' in content and 'validate' not in content:
                self.findings['medium'].append({
                    'type': 'Input Validation',
                    'file': str(route_file),
                    'issue': 'Direct JSON access without validation',
                    'recommendation': 'Validate all JSON inputs'
                })
    
    def _audit_rate_limiting(self):
        """Audit rate limiting implementation"""
        print("🚦 Auditing rate limiting...")
        
        rate_limiter_file = self.backend_path / "utils" / "rate_limiter.py"
        if rate_limiter_file.exists():
            content = rate_limiter_file.read_text()
            
            # Check thread safety
            if 'threading.Lock' not in content:
                self.findings['medium'].append({
                    'type': 'Concurrency',
                    'file': str(rate_limiter_file),
                    'issue': 'Rate limiter may not be thread-safe',
                    'recommendation': 'Use threading.Lock for thread safety'
                })
            
            # Check cleanup mechanism
            if 'clean' not in content.lower():
                self.findings['low'].append({
                    'type': 'Memory Management',
                    'file': str(rate_limiter_file),
                    'issue': 'No cleanup mechanism for old entries',
                    'recommendation': 'Implement automatic cleanup of old entries'
                })
        
        # Check rate limiting usage in routes
        emails_route = self.backend_path / "routes" / "emails.py"
        if emails_route.exists():
            content = emails_route.read_text()
            if '@ratelimit' not in content:
                self.findings['medium'].append({
                    'type': 'Rate Limiting',
                    'file': str(emails_route),
                    'issue': 'Email processing endpoint not rate limited',
                    'recommendation': 'Add rate limiting to email processing'
                })
    
    def _audit_cors_configuration(self):
        """Audit CORS configuration"""
        print("🌐 Auditing CORS configuration...")
        
        init_file = self.backend_path / "__init__.py"
        if init_file.exists():
            content = init_file.read_text()
            
            # Check for wildcard origins
            if 'origins=*' in content or "origins='*'" in content:
                self.findings['high'].append({
                    'type': 'CORS Security',
                    'file': str(init_file),
                    'issue': 'CORS allows all origins',
                    'recommendation': 'Specify exact allowed origins'
                })
            
            # Check credentials handling
            if 'supports_credentials=True' in content:
                if 'origins=' not in content or '*' in content:
                    self.findings['high'].append({
                        'type': 'CORS Credentials',
                        'file': str(init_file),
                        'issue': 'Credentials allowed with unsafe origins',
                        'recommendation': 'Only allow credentials with specific origins'
                    })
    
    def _audit_session_security(self):
        """Audit session security configuration"""
        print("🍪 Auditing session security...")
        
        init_file = self.backend_path / "__init__.py"
        if init_file.exists():
            content = init_file.read_text()
            
            security_configs = [
                ('SESSION_COOKIE_SECURE', 'Session cookies not marked secure'),
                ('SESSION_COOKIE_HTTPONLY', 'Session cookies not marked HttpOnly'),
                ('SESSION_COOKIE_SAMESITE', 'SameSite not configured for session cookies')
            ]
            
            for config, issue in security_configs:
                if config not in content:
                    self.findings['medium'].append({
                        'type': 'Session Security',
                        'file': str(init_file),
                        'issue': issue,
                        'recommendation': f'Set {config} appropriately'
                    })
    
    def _audit_database_security(self):
        """Audit database security"""
        print("🗄️ Auditing database security...")
        
        model_files = list(self.backend_path.glob("models/*.py"))
        for model_file in model_files:
            content = model_file.read_text()
            
            # Check for SQL injection vulnerabilities
            if 'text(' in content and '+' in content:
                self.findings['high'].append({
                    'type': 'SQL Injection',
                    'file': str(model_file),
                    'issue': 'Potential SQL injection in raw query',
                    'recommendation': 'Use parameterized queries'
                })
            
            # Check sensitive data handling
            if 'password' in content.lower() and 'encrypt' not in content.lower():
                self.findings['medium'].append({
                    'type': 'Data Protection',
                    'file': str(model_file),
                    'issue': 'Sensitive data may not be encrypted',
                    'recommendation': 'Encrypt sensitive database fields'
                })
    
    def _audit_api_endpoints(self):
        """Audit API endpoint security"""
        print("🔌 Auditing API endpoints...")
        
        route_files = list(self.backend_path.glob("routes/*.py"))
        for route_file in route_files:
            content = route_file.read_text()
            
            # Check for missing authentication
            routes = re.findall(r'@\w+\.route\([\'"]([^\'"]+)', content)
            jwt_protected = '@jwt_required' in content
            
            for route in routes:
                if not jwt_protected and '/health' not in route and '/auth' not in route:
                    self.findings['medium'].append({
                        'type': 'Missing Authentication',
                        'file': str(route_file),
                        'issue': f'Route {route} may lack authentication',
                        'recommendation': 'Add @jwt_required() decorator'
                    })
            
            # Check error handling
            if 'except Exception as e:' in content and 'str(e)' in content:
                self.findings['medium'].append({
                    'type': 'Information Disclosure',
                    'file': str(route_file),
                    'issue': 'Error messages may expose sensitive information',
                    'recommendation': 'Use generic error messages for users'
                })
    
    def _audit_environment_security(self):
        """Audit environment configuration security"""
        print("⚙️ Auditing environment security...")
        
        env_example = self.backend_path / "env.example"
        if env_example.exists():
            content = env_example.read_text()
            
            # Check for default/weak values
            weak_patterns = [
                ('SECRET_KEY=.*dev.*secret', 'Weak default secret key'),
                ('PASSWORD=.*password', 'Default password in example'),
                ('API_KEY=.*your-api-key', 'Default API key placeholder')
            ]
            
            for pattern, issue in weak_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.findings['low'].append({
                        'type': 'Configuration Security',
                        'file': str(env_example),
                        'issue': issue,
                        'recommendation': 'Ensure strong values in production'
                    })
    
    def _audit_dependency_vulnerabilities(self):
        """Audit dependency vulnerabilities"""
        print("📦 Auditing dependencies...")
        
        requirements_file = self.backend_path / "requirements.txt"
        if requirements_file.exists():
            try:
                # Run safety check if available
                result = subprocess.run([
                    'safety', 'check', '-r', str(requirements_file)
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0 and 'vulnerabilities found' in result.stdout:
                    self.findings['high'].append({
                        'type': 'Dependency Vulnerability',
                        'file': str(requirements_file),
                        'issue': 'Vulnerable dependencies detected',
                        'recommendation': 'Update vulnerable packages'
                    })
            except (subprocess.TimeoutExpired, FileNotFoundError):
                self.findings['info'].append({
                    'type': 'Dependency Check',
                    'file': str(requirements_file),
                    'issue': 'Could not run safety check',
                    'recommendation': 'Install safety: pip install safety'
                })
    
    def _check_code_patterns(self):
        """Check for insecure code patterns"""
        print("🔍 Checking code patterns...")
        
        py_files = list(self.backend_path.rglob("*.py"))
        js_files = list(self.frontend_path.rglob("*.ts")) + list(self.frontend_path.rglob("*.tsx"))
        
        for file_path in py_files + js_files:
            try:
                content = file_path.read_text()
                
                for category, patterns in self.security_patterns.items():
                    for pattern in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            self.findings['medium'].append({
                                'type': f'Code Pattern - {category}',
                                'file': str(file_path),
                                'line': line_num,
                                'issue': f'Potential {category.replace("_", " ")} detected',
                                'code': match.group(0)[:100],
                                'recommendation': f'Review and secure {category.replace("_", " ")}'
                            })
            except Exception as e:
                continue
    
    def _audit_file_permissions(self):
        """Audit file permissions"""
        print("📁 Auditing file permissions...")
        
        sensitive_files = [
            '.env', 'config.py', 'secrets.json'
        ]
        
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file in sensitive_files:
                    file_path = os.path.join(root, file)
                    try:
                        stat = os.stat(file_path)
                        mode = oct(stat.st_mode)[-3:]
                        
                        if mode != '600':  # Should be readable only by owner
                            self.findings['medium'].append({
                                'type': 'File Permissions',
                                'file': file_path,
                                'issue': f'Insecure permissions: {mode}',
                                'recommendation': 'Set permissions to 600 (owner read/write only)'
                            })
                    except OSError:
                        continue
    
    def _check_security_headers(self):
        """Check for security headers implementation"""
        print("🛡️ Checking security headers...")
        
        init_file = self.backend_path / "__init__.py"
        if init_file.exists():
            content = init_file.read_text()
            
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security',
                'Content-Security-Policy'
            ]
            
            missing_headers = [h for h in security_headers if h not in content]
            if missing_headers:
                self.findings['medium'].append({
                    'type': 'Security Headers',
                    'file': str(init_file),
                    'issue': f'Missing security headers: {", ".join(missing_headers)}',
                    'recommendation': 'Add security headers middleware'
                })
    
    def _generate_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        
        total_issues = sum(len(self.findings[level]) for level in self.findings)
        
        # Calculate security score
        score_weights = {'critical': -20, 'high': -10, 'medium': -5, 'low': -2, 'info': 0}
        score = max(0, 100 + sum(
            len(self.findings[level]) * weight 
            for level, weight in score_weights.items()
        ))
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project': 'Email Task Manager',
            'security_score': score,
            'total_issues': total_issues,
            'findings_by_severity': {
                level: len(issues) for level, issues in self.findings.items()
            },
            'findings': self.findings,
            'recommendations': self._generate_recommendations(),
            'summary': self._generate_summary()
        }
        
        # Save report
        report_file = self.project_root / "security_audit_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Security Audit Complete!")
        print(f"Security Score: {score}/100")
        print(f"Total Issues: {total_issues}")
        print(f"Report saved to: {report_file}")
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized security recommendations"""
        recommendations = []
        
        if self.findings['critical']:
            recommendations.append("🚨 Address critical security issues immediately")
        
        if self.findings['high']:
            recommendations.append("⚠️ Fix high-priority vulnerabilities before deployment")
        
        if len(self.findings['medium']) > 5:
            recommendations.append("🔧 Review and address medium-priority security issues")
        
        recommendations.extend([
            "🔐 Implement security headers middleware",
            "🧪 Set up automated security testing in CI/CD",
            "📊 Schedule regular security audits",
            "🔄 Implement security monitoring and alerting"
        ])
        
        return recommendations
    
    def _generate_summary(self) -> str:
        """Generate executive summary"""
        critical_count = len(self.findings['critical'])
        high_count = len(self.findings['high'])
        
        if critical_count > 0:
            return f"CRITICAL: {critical_count} critical vulnerabilities require immediate attention."
        elif high_count > 0:
            return f"WARNING: {high_count} high-priority security issues found."
        else:
            return "Security posture is generally good with minor improvements recommended."

def main():
    """Main execution function"""
    import sys
    
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    auditor = EmailTaskSecurityAuditor(project_root)
    report = auditor.run_complete_audit()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SECURITY AUDIT SUMMARY")
    print(f"{'='*60}")
    print(f"Security Score: {report['security_score']}/100")
    print(f"Critical Issues: {report['findings_by_severity']['critical']}")
    print(f"High Issues: {report['findings_by_severity']['high']}")
    print(f"Medium Issues: {report['findings_by_severity']['medium']}")
    print(f"Low Issues: {report['findings_by_severity']['low']}")
    print(f"\n{report['summary']}")
    
    return report['security_score'] >= 80

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)